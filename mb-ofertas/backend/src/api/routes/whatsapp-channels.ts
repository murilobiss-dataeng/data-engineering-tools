import { Router } from "express";
import * as channelsRepo from "../../repositories/whatsapp-channels.repository.js";

export const whatsappChannelsRouter = Router();

whatsappChannelsRouter.get("/", async (_req, res) => {
  try {
    const channels = await channelsRepo.listChannels();
    res.json({ channels });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

whatsappChannelsRouter.post("/", async (req, res) => {
  try {
    const { name, phone, channelLink } = req.body as { name?: string; phone?: string; channelLink?: string | null };
    if (!name?.trim()) {
      return res.status(400).json({ error: "name é obrigatório" });
    }
    const id = await channelsRepo.insertChannel(name.trim(), (phone || "").trim(), channelLink?.trim() || undefined);
    const channel = await channelsRepo.getChannelById(id);
    res.status(201).json(channel);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

whatsappChannelsRouter.delete("/:id", async (req, res) => {
  try {
    const deleted = await channelsRepo.deleteChannel(req.params.id);
    if (!deleted) return res.status(404).json({ error: "Canal não encontrado" });
    res.json({ deleted: true });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
