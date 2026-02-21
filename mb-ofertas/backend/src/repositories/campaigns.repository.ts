import { query } from "../db/client.js";

export async function createCampaign(data: {
  name: string;
  productIds: string[];
  targetType: "list" | "group" | "broadcast";
  targetRef?: string | null;
  scheduledAt?: Date | null;
}) {
  const res = await query<{ id: string }>(
    `INSERT INTO campaigns (name, product_ids, target_type, target_ref, status, scheduled_at)
     VALUES ($1, $2, $3, $4, $5, $6)
     RETURNING id`,
    [
      data.name,
      data.productIds,
      data.targetType,
      data.targetRef ?? null,
      data.scheduledAt ? "scheduled" : "draft",
      data.scheduledAt ?? null,
    ]
  );
  return res.rows[0].id;
}

export async function getCampaignById(id: string) {
  const res = await query(
    `SELECT id, name, status, scheduled_at, started_at, completed_at, product_ids, target_type, target_ref, created_at
     FROM campaigns WHERE id = $1`,
    [id]
  );
  return res.rows[0] ?? null;
}

export async function listCampaigns(limit = 50, offset = 0) {
  const res = await query(
    `SELECT id, name, status, scheduled_at, started_at, completed_at, product_ids, target_type, created_at
     FROM campaigns ORDER BY created_at DESC LIMIT $1 OFFSET $2`,
    [limit, offset]
  );
  return res.rows;
}

export async function updateCampaignStatus(
  id: string,
  status: "draft" | "scheduled" | "sending" | "completed" | "cancelled"
) {
  await query(
    `UPDATE campaigns SET status = $1, updated_at = now(),
     started_at = CASE WHEN $1 = 'sending' THEN COALESCE(started_at, now()) ELSE started_at END,
     completed_at = CASE WHEN $1 = 'completed' THEN now() ELSE completed_at END
     WHERE id = $2`,
    [status, id]
  );
}

export async function insertMessage(data: {
  campaignId: string;
  productId: string;
  body: string;
  shortLink?: string | null;
  recipient?: string | null;
}) {
  const res = await query<{ id: string }>(
    `INSERT INTO messages (campaign_id, product_id, body, short_link, recipient, status)
     VALUES ($1, $2, $3, $4, $5, 'pending') RETURNING id`,
    [
      data.campaignId,
      data.productId,
      data.body,
      data.shortLink ?? null,
      data.recipient ?? null,
    ]
  );
  return res.rows[0].id;
}
