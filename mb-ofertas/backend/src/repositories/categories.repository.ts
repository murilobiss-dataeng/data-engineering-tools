import { query } from "../db/client.js";

export async function getCategoryBySlug(slug: string): Promise<{ id: string; name: string; slug: string } | null> {
  const res = await query<{ id: string; name: string; slug: string }>(
    `SELECT id, name, slug FROM categories WHERE slug = $1 AND is_active = true`,
    [slug]
  );
  return res.rows[0] ?? null;
}

export async function listCategories(): Promise<{ id: string; name: string; slug: string }[]> {
  const res = await query<{ id: string; name: string; slug: string }>(
    `SELECT id, name, slug FROM categories WHERE is_active = true ORDER BY name`
  );
  return res.rows;
}
