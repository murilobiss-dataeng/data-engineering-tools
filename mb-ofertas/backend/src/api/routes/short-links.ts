import { Router } from "express";
import { getLongUrlByCode } from "../../repositories/short-links.repository.js";

export const shortLinksRouter = Router();

/** Retorna a URL longa para um código (usado pelo frontend em /r/[code] para redirecionar). */
shortLinksRouter.get("/:code", async (req, res) => {
  try {
    const code = req.params.code?.trim();
    if (!code || code.length > 20) return res.status(404).json({ error: "Link não encontrado" });
    const longUrl = await getLongUrlByCode(code);
    if (!longUrl) return res.status(404).json({ error: "Link não encontrado" });
    res.json({ url: longUrl });
  } catch {
    res.status(500).json({ error: "Erro ao buscar link" });
  }
});
