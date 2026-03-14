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
 * Gera chave única para um post (evita duplicar por url).
 */
export function postKey(post) {
  return post.url || `${post.title || ""}_${post.text?.slice(0, 50) || ""}`;
}
