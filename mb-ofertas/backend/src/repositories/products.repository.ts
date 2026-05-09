import { query } from "../db/client.js";
import type { ProductInput } from "../services/products/types.js";
import { roundToTwoDecimals } from "../utils/price.js";

/** Mesmo produto com query string / fragmento diferente (ex.: outro tag=) → mesma chave. */
export function affiliateLinkBaseForDedupe(affiliateLink: string): string {
  const s = String(affiliateLink ?? "").trim();
  if (!s) return "";
  const qi = s.indexOf("?");
  const hi = s.indexOf("#");
  let cut = s.length;
  if (qi >= 0) cut = Math.min(cut, qi);
  if (hi >= 0) cut = Math.min(cut, hi);
  return s.slice(0, cut).replace(/\/$/, "").toLowerCase();
}

/** Retorna o id do produto se já existir um com o mesmo link de afiliado (evita duplicata). */
export async function findProductIdByAffiliateLink(affiliateLink: string): Promise<string | null> {
  const res = await query<{ id: string }>(
    `SELECT id FROM products WHERE affiliate_link = $1 LIMIT 1`,
    [affiliateLink]
  );
  return res.rows[0]?.id ?? null;
}

/** Mesmo link ignorando ?query e #fragment (evita duplicata na busca automática). */
export async function findProductIdByAffiliateNormalized(affiliateLink: string): Promise<string | null> {
  const base = affiliateLinkBaseForDedupe(affiliateLink);
  if (!base) return null;
  const res = await query<{ id: string }>(
    `SELECT id FROM products
     WHERE lower(regexp_replace(regexp_replace(trim(affiliate_link), '[?#].*$', ''), '/$', '')) = $1
     LIMIT 1`,
    [base]
  );
  return res.rows[0]?.id ?? null;
}

/** Retorna o id do produto se já existir com o mesmo external_id e source. */
export async function findProductIdByExternalAndSource(
  externalId: string,
  source: string
): Promise<string | null> {
  const res = await query<{ id: string }>(
    `SELECT id FROM products WHERE external_id = $1 AND source = $2 LIMIT 1`,
    [externalId, source]
  );
  return res.rows[0]?.id ?? null;
}

export async function insertProduct(
  input: ProductInput & { categoryId?: string | null }
): Promise<{ id: string; isNew: boolean }> {
  const existingByLink = await findProductIdByAffiliateLink(input.affiliateLink);
  if (existingByLink) return { id: existingByLink, isNew: false };

  const existingByNorm = await findProductIdByAffiliateNormalized(input.affiliateLink);
  if (existingByNorm) return { id: existingByNorm, isNew: false };

  if (input.externalId && (input.source ?? "amazon")) {
    const existingByExternal = await findProductIdByExternalAndSource(
      input.externalId,
      input.source ?? "amazon"
    );
    if (existingByExternal) return { id: existingByExternal, isNew: false };
  }

  const res = await query<{ id: string }>(
    `INSERT INTO products (
      category_id, external_id, title, price, previous_price, discount_pct,
      affiliate_link, image_url, source, status, installments,
      installment_max_times, installment_unit_price
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'pending', $10, $11, $12)
    RETURNING id`,
    [
      input.categoryId ?? null,
      input.externalId ?? null,
      input.title,
      roundToTwoDecimals(Number(input.price)),
      input.previousPrice != null ? roundToTwoDecimals(Number(input.previousPrice)) : null,
      input.discountPct != null ? roundToTwoDecimals(Number(input.discountPct)) : null,
      input.affiliateLink,
      input.imageUrl ?? null,
      input.source ?? "amazon",
      input.installments ?? null,
      input.installmentMaxTimes != null && input.installmentMaxTimes > 0 ? Math.floor(Number(input.installmentMaxTimes)) : null,
      input.installmentUnitPrice != null ? roundToTwoDecimals(Number(input.installmentUnitPrice)) : null,
    ]
  );
  return { id: res.rows[0].id, isNew: true };
}

export async function listProducts(filters?: {
  status?: string;
  /** Se definido, filtra por vários status (ex.: fila do painel: pending + approved). */
  statuses?: string[];
  categoryId?: string;
  limit?: number;
  offset?: number;
}) {
  const limit = filters?.limit ?? 50;
  const offset = filters?.offset ?? 0;
  const conditions: string[] = [];
  const params: unknown[] = [];
  let i = 1;

  if (filters?.statuses?.length) {
    conditions.push(`p.status = ANY($${i++}::varchar[])`);
    params.push(filters.statuses);
  } else if (filters?.status) {
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
            p.installment_max_times, p.installment_unit_price, p.coupon,
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
            p.installment_max_times, p.installment_unit_price, p.coupon,
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
  const statusVal = String(status);
  await query(
    `UPDATE products SET status = CAST($1 AS character varying(20)), updated_at = now(), approved_at = CASE WHEN CAST($2 AS character varying(20)) = 'approved' THEN now() ELSE approved_at END, approved_by = $3 WHERE id = $4`,
    [statusVal, statusVal, approvedBy ?? null, id]
  );
}

/** Remove o produto do banco (uso administrativo; a fila do painel usa status rejected). */
export async function deleteProduct(id: string): Promise<boolean> {
  const res = await query(`DELETE FROM products WHERE id = $1`, [id]);
  return (res.rowCount ?? 0) > 0;
}

/** Fila para o bot WhatsApp: pendentes (sem aprovação manual) e aprovados legados. */
export async function getApprovedProducts(limit = 20, channelSlug?: string | null) {
  const slug = channelSlug?.trim() || null;
  const res = await query(
    `SELECT p.id, p.title, p.price, p.previous_price, p.discount_pct, p.affiliate_link, p.image_url, p.installments,
            p.installment_max_times, p.installment_unit_price, p.coupon,
            c.slug AS category_slug
     FROM products p
     LEFT JOIN categories c ON c.id = p.category_id
     WHERE p.status IN ('pending', 'approved')
     AND ($1::text IS NULL OR $1 = '' OR c.slug = $1)
     ORDER BY
       (p.discount_pct IS NULL OR p.discount_pct <= 0) ASC,
       p.discount_pct DESC NULLS LAST,
       COALESCE(p.approved_at, p.created_at) DESC NULLS LAST
     LIMIT $2`,
    [slug, limit]
  );
  return res.rows;
}

/**
 * Ofertas aprovadas há mais de X horas sem uso: marca como rejeitadas (mantém linha para dedupe).
 */
export async function expireApprovedOlderThanHours(hours: number): Promise<number> {
  const res = await query(
    `UPDATE products
     SET status = 'rejected', updated_at = now()
     WHERE status = 'approved'
     AND approved_at IS NOT NULL
     AND approved_at < now() - ($1 || ' hours')::interval`,
    [hours]
  );
  return res.rowCount ?? 0;
}

export async function updateProductCoupon(id: string, coupon: string | null): Promise<boolean> {
  const v = coupon != null && String(coupon).trim() !== "" ? String(coupon).trim() : null;
  const res = await query(`UPDATE products SET coupon = $1, updated_at = now() WHERE id = $2`, [v, id]);
  return (res.rowCount ?? 0) > 0;
}
