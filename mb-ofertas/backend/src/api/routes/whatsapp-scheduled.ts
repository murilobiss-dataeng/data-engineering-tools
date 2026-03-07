import { Router } from "express";
import * as scheduledRepo from "../../repositories/whatsapp-scheduled.repository.js";
import { getCampaignWhatsAppMessage } from "../../services/campaigns/campaign-whatsapp-message.service.js";

export const whatsappScheduledRouter = Router();

whatsappScheduledRouter.get("/", async (_req, res) => {
  try {
    const list = await scheduledRepo.listScheduled();
    res.json({ scheduled: list });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

whatsappScheduledRouter.post("/", async (req, res) => {
  try {
    const { channelId, message, scheduledAt } = req.body as {
      channelId?: string;
      message?: string;
      scheduledAt?: string;
    };
    if (!channelId?.trim() || !message?.trim() || !scheduledAt) {
      return res.status(400).json({ error: "channelId, message e scheduledAt são obrigatórios" });
    }
    const at = new Date(scheduledAt);
    if (Number.isNaN(at.getTime())) {
      return res.status(400).json({ error: "scheduledAt inválido" });
    }
    const id = await scheduledRepo.insertScheduled(channelId.trim(), message.trim(), at);
    const row = await scheduledRepo.getScheduledById(id);
    res.status(201).json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Programação em massa: várias campanhas com intervalo (ex.: 10 min) entre cada post. */
whatsappScheduledRouter.post("/bulk", async (req, res) => {
  try {
    const { channelId, campaignIds, startAt, intervalMinutes } = req.body as {
      channelId?: string;
      campaignIds?: string[];
      startAt?: string;
      intervalMinutes?: number;
    };
    if (!channelId?.trim() || !Array.isArray(campaignIds) || campaignIds.length === 0 || !startAt) {
      return res.status(400).json({
        error: "channelId, campaignIds (array não vazio) e startAt são obrigatórios",
      });
    }
    const start = new Date(startAt);
    if (Number.isNaN(start.getTime())) {
      return res.status(400).json({ error: "startAt inválido" });
    }
    const interval = Math.max(1, Math.min(60, intervalMinutes ?? 10));
    const shortLinkBaseUrl = (req.get("X-Short-Link-Base") || req.get("x-short-link-base") || "").trim() || undefined;
    const ids: string[] = [];
    for (let i = 0; i < campaignIds.length; i++) {
      const cid = campaignIds[i];
      if (!cid || typeof cid !== "string") continue;
      try {
        const message = await getCampaignWhatsAppMessage(cid, { shortLinkBaseUrl });
        const at = new Date(start.getTime() + i * interval * 60 * 1000);
        const id = await scheduledRepo.insertScheduled(channelId.trim(), message, at);
        ids.push(id);
      } catch (e) {
        // skip campanha inexistente ou erro
      }
    }
    res.status(201).json({ created: ids.length, ids });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

whatsappScheduledRouter.post("/:id/open", async (req, res) => {
  try {
    const row = await scheduledRepo.getScheduledById(req.params.id);
    if (!row) return res.status(404).json({ error: "Agendamento não encontrado" });
    await scheduledRepo.markOpened(req.params.id);
    const phone = row.channel_phone.startsWith("55") ? row.channel_phone : "55" + row.channel_phone;
    const channelLink = row.channel_link?.trim() || null;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.json({
      message: row.message,
      channelPhone: phone,
      channelLink: channelLink,
      url: channelLink
        ? null
        : `https://wa.me/${phone}?text=${encodeURIComponent(row.message)}`,
    });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
