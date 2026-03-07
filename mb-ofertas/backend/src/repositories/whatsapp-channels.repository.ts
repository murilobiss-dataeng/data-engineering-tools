import { query } from "../db/client.js";

export type WhatsAppChannel = {
  id: string;
  name: string;
  phone: string;
  channel_link: string | null;
  created_at: string;
};

export async function listChannels(): Promise<WhatsAppChannel[]> {
  const res = await query<{ id: string; name: string; phone: string; channel_link: string | null; created_at: string }>(
    `SELECT id, name, phone, channel_link, created_at FROM whatsapp_channels ORDER BY name`
  );
  return res.rows.map((r) => ({ ...r, channel_link: r.channel_link?.trim() || null }));
}

export async function insertChannel(name: string, phone: string, channelLink?: string | null): Promise<string> {
  const link = channelLink?.trim() || null;
  const digits = (phone || "").replace(/\D/g, "").trim();
  if (!link && digits.length < 10) throw new Error("Informe um número (DDD + número) ou link do canal.");
  const res = await query<{ id: string }>(
    `INSERT INTO whatsapp_channels (name, phone, channel_link) VALUES ($1, $2, $3) RETURNING id`,
    [name.trim(), digits || "", link]
  );
  return res.rows[0].id;
}

export async function deleteChannel(id: string): Promise<boolean> {
  const res = await query(`DELETE FROM whatsapp_channels WHERE id = $1`, [id]);
  return (res.rowCount ?? 0) > 0;
}

export async function getChannelById(id: string): Promise<WhatsAppChannel | null> {
  const res = await query<WhatsAppChannel & { channel_link: string | null }>(
    `SELECT id, name, phone, channel_link, created_at FROM whatsapp_channels WHERE id = $1`,
    [id]
  );
  const r = res.rows[0];
  if (!r) return null;
  return { ...r, channel_link: r.channel_link ?? null };
}
