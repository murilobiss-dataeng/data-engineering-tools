import { Router } from "express";
import { query } from "../../db/client.js";

export const categoriesRouter = Router();

categoriesRouter.get("/", async (_req, res) => {
  try {
    const result = await query(
      `SELECT id, name, slug, is_active, created_at FROM categories WHERE is_active = true ORDER BY name`
    );
    res.json({ categories: result.rows });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
