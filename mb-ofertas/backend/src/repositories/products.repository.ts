import { query } from "../db/client.js";
import type { ProductInput } from "../services/products/types.js";

export async function insertProduct(
  input: ProductInput & { categoryId?: string | null }
): Promise<string> {
  const res = await query<{ id: string }>(
    `INSERT INTO products (
      category_id, external_id, title, price, previous_price, discount_pct,
      affiliate_link, image_url, source, status, installments
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'pending', $10)
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
      input.installments ?? null,
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
    conditions.push(`p.status = $${i++}`);
    params.push(filters.status);
  }
  if (filters?.categoryId) {
    conditions.push(`p.category_id = $${i++}`);
    params.push(filters.categoryId);
  }

  const where = conditions.length ? `WHERE ${conditions.join(" AND ")}` : "";
  params.push(limit, offset);

  const res = await query(
    `SELECT p.id, p.category_id, p.external_id, p.title, p.price, p.previous_price, p.discount_pct,
            p.affiliate_link, p.image_url, p.source, p.status, p.approved_at, p.created_at, p.updated_at, p.installments,
            c.name AS category_name, c.slug AS category_slug
     FROM products p
     LEFT JOIN categories c ON c.id = p.category_id
     ${where}
     ORDER BY p.created_at DESC
     LIMIT $${i} OFFSET $${i + 1}`,
    params
  );
  return res.rows;
}

export async function getProductById(id: string) {
  const res = await query(
    `SELECT p.id, p.category_id, p.external_id, p.title, p.price, p.previous_price, p.discount_pct,
            p.affiliate_link, p.image_url, p.source, p.status, p.approved_at, p.created_at, p.updated_at, p.installments,
            c.name AS category_name, c.slug AS category_slug
     FROM products p
     LEFT JOIN categories c ON c.id = p.category_id
     WHERE p.id = $1`,
    [id]
  );
  return res.rows[0] ?? null;
}

export async function updateProductCategory(id: string, categoryId: string | null): Promise<boolean> {
  const res = await query(`UPDATE products SET category_id = $1, updated_at = now() WHERE id = $2`, [
    categoryId,
    id,
  ]);
  return (res.rowCount ?? 0) > 0;
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

/** Remove o produto do banco (usado ao reprovar = tirar da lista). */
export async function deleteProduct(id: string): Promise<boolean> {
  const res = await query(`DELETE FROM products WHERE id = $1`, [id]);
  return (res.rowCount ?? 0) > 0;
}

export async function getApprovedProducts(limit = 20) {
  const res = await query(
    `SELECT id, title, price, previous_price, discount_pct, affiliate_link, image_url, installments
     FROM products WHERE status = 'approved' ORDER BY approved_at DESC NULLS LAST LIMIT $1`,
    [limit]
  );
  return res.rows;
}
