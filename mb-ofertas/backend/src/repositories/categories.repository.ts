import { query } from "../db/client.js";

const DEFAULT_CATEGORIES = [
  ["Health", "health"],
  ["Tech", "tech"],
  ["Ofertas", "ofertas"],
  ["Faith", "faith"],
  ["Fitness", "fitness"],
];

async function ensureDefaultCategories(): Promise<void> {
  await query(
    `INSERT INTO categories (name, slug)
     VALUES ('Health', 'health'),
            ('Tech', 'tech'),
            ('Ofertas', 'ofertas'),
            ('Faith', 'faith'),
            ('Fitness', 'fitness')
     ON CONFLICT (slug) DO NOTHING`
  );
}

export async function getCategoryBySlug(slug: string): Promise<{ id: string; name: string; slug: string } | null> {
  await ensureDefaultCategories();
  const res = await query<{ id: string; name: string; slug: string }>(
    `SELECT id, name, slug FROM categories WHERE slug = $1 AND is_active = true`,
    [slug]
  );
  return res.rows[0] ?? null;
}

export async function listCategories(): Promise<{ id: string; name: string; slug: string }[]> {
  await ensureDefaultCategories();
  const res = await query<{ id: string; name: string; slug: string }>(
    `SELECT id, name, slug FROM categories WHERE is_active = true ORDER BY name`
  );
  const preferredOrder = DEFAULT_CATEGORIES.map(([, slug]) => slug);
  return res.rows.sort((a, b) => {
    const ia = preferredOrder.indexOf(a.slug);
    const ib = preferredOrder.indexOf(b.slug);
    return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
  });
}
