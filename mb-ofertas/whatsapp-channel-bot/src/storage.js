import fs from "fs";
import path from "path";

const SENT_FILE = "sent_posts.json";

/**
 * Armazena quais posts já foram enviados (por url ou id) para evitar duplicados.
 * Usa um JSON local na pasta configurada em dataPath.
 */
export function getSentFilePath(dataPath) {
  return path.join(dataPath, SENT_FILE);
}

function ensureDataDir(dataPath) {
  if (!fs.existsSync(dataPath)) {
    fs.mkdirSync(dataPath, { recursive: true });
  }
}

/**
 * Lê a lista de chaves já enviadas (urls ou ids).
 */
export function loadSentIds(dataPath) {
  const file = getSentFilePath(dataPath);
  ensureDataDir(dataPath);
  if (!fs.existsSync(file)) {
    return [];
  }
  try {
    const data = JSON.parse(fs.readFileSync(file, "utf-8"));
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

/**
 * Marca uma chave como enviada e persiste no disco.
 */
export function markAsSent(dataPath, key) {
  const file = getSentFilePath(dataPath);
  const ids = loadSentIds(dataPath);
  if (ids.includes(key)) return;
  ids.push(key);
  ensureDataDir(dataPath);
  fs.writeFileSync(file, JSON.stringify(ids, null, 2), "utf-8");
}

/**
 * Mesma URL de afiliado com parâmetros diferentes → mesma chave (alinha com o backend na inserção).
 */
export function affiliateLinkBaseForDedupe(url) {
  const s = String(url ?? "").trim();
  if (!s) return "";
  const qi = s.indexOf("?");
  const hi = s.indexOf("#");
  let cut = s.length;
  if (qi >= 0) cut = Math.min(cut, qi);
  if (hi >= 0) cut = Math.min(cut, hi);
  return s.slice(0, cut).replace(/\/$/, "").toLowerCase();
}

/**
 * Chave estável para deduplicar envios: id da API (preferido), senão URL base, senão título+trecho do texto.
 */
export function postKey(post) {
  const id = post?.id != null && String(post.id).trim() !== "" ? String(post.id).trim() : "";
  if (id) return `id:${id}`;
  const u = post.url && String(post.url).trim();
  if (u) return `u:${affiliateLinkBaseForDedupe(u)}`;
  const t = (post.title || "").trim();
  const snippet = String(post.text || "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 80);
  return `t:${t}|${snippet}`;
}
