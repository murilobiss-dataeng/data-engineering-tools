import { Router } from "express";
import * as scheduledRepo from "../../repositories/whatsapp-scheduled.repository.js";

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

whatsappScheduledRouter.post("/:id/open", async (req, res) => {
  try {
    const row = await scheduledRepo.getScheduledById(req.params.id);
    if (!row) return res.status(404).json({ error: "Agendamento não encontrado" });
    await scheduledRepo.markOpened(req.params.id);
    res.json({ url: `https://wa.me/${row.channel_phone.startsWith("55") ? row.channel_phone : "55" + row.channel_phone}?text=${encodeURIComponent(row.message)}` });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
