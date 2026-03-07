import { Router } from "express";
import { getLogs, appendLog } from "../lib/log-buffer.js";

export const logsRouter = Router();

logsRouter.get("/", (req, res) => {
  try {
    const limit = Math.min(Number(req.query?.limit) || 200, 500);
    const entries = getLogs(limit);
    res.json({ logs: entries });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Permite colar logs (ex.: erros do ML) para enviar ao suporte. */
logsRouter.post("/", (req, res) => {
  try {
    const { message } = req.body as { message?: string };
    const text = typeof message === "string" ? message.trim() : "";
    if (text) appendLog("user", text);
    res.status(201).json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
