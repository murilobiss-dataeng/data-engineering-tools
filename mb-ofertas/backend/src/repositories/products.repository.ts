import { query } from "../db/client.js";
import type { ProductInput } from "../services/products/types.js";

export async function insertProduct(
  input: ProductInput & { categoryId?: string | null }
): Promise<string> {
  const res = await query<{ id: string }>(
    `INSERT INTO products (
      category_id, external_id, title, price, previous_price, discount_pct,
      affiliate_link, image_url, source, status
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'pending')
    RETURNING id`,
    [
      input.categoryId ?? null,
      input.externalId ?? null,
      input.title,
      input.price,
      input.previousPrice ?? null,
      input.discountPct ?? null,
      input.affiliateLink,
      input.imageUrl ?? null,
      input.source ?? "amazon",
    ]
  );
  return res.rows[0].id;
}

export async function listProducts(filters?: {
  status?: string;
  categoryId?: string;
  limit?: number;
  offset?: number;
}) {
  const limit = filters?.limit ?? 50;
  const offset = filters?.offset ?? 0;
  const conditions: string[] = [];
  const params: unknown[] = [];
  let i = 1;

  if (filters?.status) {
    conditions.push(`status = $${i++}`);
    params.push(filters.status);
  }
  if (filters?.categoryId) {
    conditions.push(`category_id = $${i++}`);
    params.push(filters.categoryId);
  }

  const where = conditions.length ? `WHERE ${conditions.join(" AND ")}` : "";
  params.push(limit, offset);

  const res = await query(
    `SELECT id, category_id, external_id, title, price, previous_price, discount_pct,
            affiliate_link, image_url, source, status, approved_at, created_at, updated_at
     FROM products ${where}
     ORDER BY created_at DESC
     LIMIT $${i} OFFSET $${i + 1}`,
    params
  );
  return res.rows;
}

export async function getProductById(id: string) {
  const res = await query(
    `SELECT id, category_id, external_id, title, price, previous_price, discount_pct,
            affiliate_link, image_url, source, status, approved_at, created_at, updated_at
     FROM products WHERE id = $1`,
    [id]
  );
  return res.rows[0] ?? null;
}

export async function updateProductStatus(
  id: string,
  status: "approved" | "rejected" | "sent",
  approvedBy?: string
) {
  await query(
    `UPDATE products SET status = $1, updated_at = now(), approved_at = CASE WHEN $1 = 'approved' THEN now() ELSE approved_at END, approved_by = $2 WHERE id = $3`,
    [status, approvedBy ?? null, id]
  );
}

export async function getApprovedProducts(limit = 20) {
  const res = await query(
    `SELECT id, title, price, previous_price, discount_pct, affiliate_link, image_url
     FROM products WHERE status = 'approved' ORDER BY approved_at DESC NULLS LAST LIMIT $1`,
    [limit]
  );
  return res.rows;
}
