/**
 * WhatsApp Business API - envio de mensagens.
 * Compatível com Twilio, 360dialog ou outro provedor que exponha API REST.
 * Configure WHATSAPP_* no .env conforme seu provedor.
 */
import { env } from "../../config/env.js";
import { logger } from "../../config/logger.js";

const FROM = env.WHATSAPP_FROM_NUMBER;
const ACCOUNT_SID = env.WHATSAPP_ACCOUNT_SID;
const AUTH_TOKEN = env.WHATSAPP_AUTH_TOKEN;
const PHONE_ID = env.WHATSAPP_PHONE_NUMBER_ID;

export type SendMessageResult = { success: boolean; messageId?: string; error?: string };

/**
 * Envia mensagem de texto para um número WhatsApp.
 * Implementação exemplo com Twilio; ajuste para seu provedor.
 */
export async function sendWhatsAppText(to: string, body: string): Promise<SendMessageResult> {
  const normalizedTo = to.replace(/\D/g, "");
  const toE164 = normalizedTo.startsWith("55") ? `+${normalizedTo}` : `+55${normalizedTo}`;

  if (!FROM || !ACCOUNT_SID || !AUTH_TOKEN) {
    logger.warn("WhatsApp: credenciais não configuradas. Simulando envio.");
    logger.debug({ to: toE164, bodyLength: body.length }, "send (dry-run)");
    return { success: true, messageId: `dry-${Date.now()}` };
  }

  try {
    // Twilio: POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json
    const auth = Buffer.from(`${ACCOUNT_SID}:${AUTH_TOKEN}`).toString("base64");
    const form = new URLSearchParams({
      To: `whatsapp:${toE164}`,
      From: `whatsapp:${FROM}`,
      Body: body,
    });

    const res = await fetch(
      `https://api.twilio.com/2010-04-01/Accounts/${ACCOUNT_SID}/Messages.json`,
      {
        method: "POST",
        headers: {
          Authorization: `Basic ${auth}`,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: form.toString(),
      }
    );

    const data = (await res.json()) as { sid?: string; message?: string; error_message?: string };

    if (!res.ok) {
      logger.error({ status: res.status, data }, "WhatsApp send error");
      return { success: false, error: data.message ?? data.error_message ?? String(res.status) };
    }

    logger.info({ to: toE164, messageId: data.sid }, "WhatsApp sent");
    return { success: true, messageId: data.sid };
  } catch (err) {
    logger.error({ err, to: toE164 }, "WhatsApp send exception");
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

/**
 * Verifica se o módulo está configurado para envio real.
 */
export function isWhatsAppConfigured(): boolean {
  return !!(FROM && (ACCOUNT_SID || PHONE_ID));
}
