import { query } from "../db/client.js";

export type WhatsAppScheduled = {
  id: string;
  channel_id: string;
  message: string;
  scheduled_at: string;
  status: string;
  opened_at: string | null;
  created_at: string;
  channel_name?: string;
  channel_phone?: string;
};

export async function insertScheduled(
  channelId: string,
  message: string,
  scheduledAt: Date
): Promise<string> {
  const res = await query<{ id: string }>(
    `INSERT INTO whatsapp_scheduled (channel_id, message, scheduled_at) VALUES ($1, $2, $3) RETURNING id`,
    [channelId, message, scheduledAt]
  );
  return res.rows[0].id;
}

export async function listScheduled(limit = 50): Promise<WhatsAppScheduled[]> {
  const res = await query<WhatsAppScheduled & { channel_name: string; channel_phone: string }>(
    `SELECT s.id, s.channel_id, s.message, s.scheduled_at, s.status, s.opened_at, s.created_at,
            c.name AS channel_name, c.phone AS channel_phone
     FROM whatsapp_scheduled s
     JOIN whatsapp_channels c ON c.id = s.channel_id
     ORDER BY s.scheduled_at ASC
     LIMIT $1`,
    [limit]
  );
  return res.rows;
}

export async function getScheduledById(id: string): Promise<(WhatsAppScheduled & { channel_phone: string; channel_link?: string | null }) | null> {
  const res = await query<WhatsAppScheduled & { channel_phone: string; channel_link?: string | null }>(
    `SELECT s.id, s.channel_id, s.message, s.scheduled_at, s.status, s.opened_at, s.created_at,
            c.phone AS channel_phone, c.channel_link AS channel_link
     FROM whatsapp_scheduled s
     JOIN whatsapp_channels c ON c.id = s.channel_id
     WHERE s.id = $1`,
    [id]
  );
  return res.rows[0] ?? null;
}

export async function markOpened(id: string): Promise<boolean> {
  const res = await query(
    `UPDATE whatsapp_scheduled SET status = 'opened', opened_at = now() WHERE id = $1`,
    [id]
  );
  return (res.rowCount ?? 0) > 0;
}
