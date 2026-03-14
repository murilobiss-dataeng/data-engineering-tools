/**
 * Monta a mensagem formatada para WhatsApp.
 *
 * 🙏 *{title}*
 *
 * {text}
 *
 * Leia completo:
 * {url}
 */
export function formatMessage(post) {
  const title = post.title || "Post";
  const text = post.text || "";
  const url = post.url || "";
  const parts = [`🙏 *${title}*`, "", text.trim(), ""];
  if (url) {
    parts.push("Leia completo:");
    parts.push(url);
  }
  return parts.join("\n").trim();
}
