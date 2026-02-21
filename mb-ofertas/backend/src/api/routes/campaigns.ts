import { Router } from "express";
import * as campaignsRepo from "../../repositories/campaigns.repository.js";
import * as productsRepo from "../../repositories/products.repository.js";
import { generateOfferMessage } from "../../services/messages/copy-generator.js";
import { addSendJob } from "../../workers/queues.js";

export const campaignsRouter = Router();

campaignsRouter.get("/", async (req, res) => {
  try {
    const limit = Math.min(Number(req.query.limit) || 50, 100);
    const offset = Number(req.query.offset) || 0;
    const rows = await campaignsRepo.listCampaigns(limit, offset);
    res.json({ campaigns: rows });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

campaignsRouter.get("/:id", async (req, res) => {
  try {
    const row = await campaignsRepo.getCampaignById(req.params.id);
    if (!row) return res.status(404).json({ error: "Campanha não encontrada" });
    res.json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

campaignsRouter.post("/", async (req, res) => {
  try {
    const { name, productIds, targetType, targetRef, scheduledAt } = req.body as {
      name?: string;
      productIds?: string[];
      targetType?: string;
      targetRef?: string;
      scheduledAt?: string;
    };
    if (!name || !Array.isArray(productIds)) {
      return res.status(400).json({ error: "name e productIds são obrigatórios" });
    }
    const id = await campaignsRepo.createCampaign({
      name,
      productIds,
      targetType: targetType === "group" ? "group" : targetType === "broadcast" ? "broadcast" : "list",
      targetRef: targetRef ?? null,
      scheduledAt: scheduledAt ? new Date(scheduledAt) : null,
    });
    const row = await campaignsRepo.getCampaignById(id);
    res.status(201).json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/**
 * Enviar agora: cria mensagens, enfileira jobs para cada destinatário.
 * Body: { recipientPhones: string[] } (lista de números com DDD)
 */
campaignsRouter.post("/:id/send-now", async (req, res) => {
  try {
    const campaign = await campaignsRepo.getCampaignById(req.params.id);
    if (!campaign) return res.status(404).json({ error: "Campanha não encontrada" });
    if (campaign.status === "sending" || campaign.status === "completed") {
      return res.status(400).json({ error: "Campanha já enviada ou em envio" });
    }

    const { recipientPhones } = req.body as { recipientPhones?: string[] };
    if (!Array.isArray(recipientPhones) || recipientPhones.length === 0) {
      return res.status(400).json({ error: "recipientPhones (array de números) é obrigatório" });
    }

    const productIds = campaign.product_ids as string[];
    const products = await Promise.all(
      productIds.map((id) => productsRepo.getProductById(id))
    ).then((rows) => rows.filter(Boolean));

    if (products.length === 0) {
      return res.status(400).json({ error: "Nenhum produto aprovado na campanha" });
    }

    await campaignsRepo.updateCampaignStatus(req.params.id, "sending");

    let delayMs = 0;
    const messageIds: string[] = [];

    for (const product of products) {
      const body = generateOfferMessage({
        title: product.title,
        price: parseFloat(product.price),
        previousPrice: product.previous_price ? parseFloat(product.previous_price) : null,
        discountPct: product.discount_pct ? parseFloat(product.discount_pct) : null,
        affiliateLink: product.affiliate_link,
        imageUrl: product.image_url,
      });

      for (const phone of recipientPhones) {
        const messageId = await campaignsRepo.insertMessage({
          campaignId: req.params.id,
          productId: product.id,
          body,
          recipient: phone,
        });
        messageIds.push(messageId);
        await addSendJob(
          {
            campaignId: req.params.id,
            productId: product.id,
            recipient: phone,
            body,
            messageId,
          },
          delayMs
        );
        delayMs += 6000; // 6s entre mensagens (anti-ban)
      }
    }

    res.json({
      ok: true,
      campaignId: req.params.id,
      messagesQueued: messageIds.length,
      recipients: recipientPhones.length,
      products: products.length,
    });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
