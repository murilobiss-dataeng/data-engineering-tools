import { query } from "../db/client.js";

export type WhatsAppChannel = {
  id: string;
  name: string;
  phone: string;
  created_at: string;
};

export async function listChannels(): Promise<WhatsAppChannel[]> {
  const res = await query<WhatsAppChannel>(
    `SELECT id, name, phone, created_at FROM whatsapp_channels ORDER BY name`
  );
  return res.rows;
}

export async function insertChannel(name: string, phone: string): Promise<string> {
  const digits = phone.replace(/\D/g, "").trim();
  if (digits.length < 10) throw new Error("Número inválido (mínimo 10 dígitos com DDD).");
  const res = await query<{ id: string }>(
    `INSERT INTO whatsapp_channels (name, phone) VALUES ($1, $2) RETURNING id`,
    [name.trim(), digits]
  );
  return res.rows[0].id;
}

export async function deleteChannel(id: string): Promise<boolean> {
  const res = await query(`DELETE FROM whatsapp_channels WHERE id = $1`, [id]);
  return (res.rowCount ?? 0) > 0;
}

export async function getChannelById(id: string): Promise<WhatsAppChannel | null> {
  const res = await query<WhatsAppChannel>(
    `SELECT id, name, phone, created_at FROM whatsapp_channels WHERE id = $1`,
    [id]
  );
  return res.rows[0] ?? null;
}
