/**
 * Monta a mensagem para WhatsApp: apenas o texto do post (já vem com título, preço e link da API).
 * Sem título duplicado e sem bloco "Leia completo".
 */
export function formatMessage(post) {
  return (post.text || "").trim();
}
