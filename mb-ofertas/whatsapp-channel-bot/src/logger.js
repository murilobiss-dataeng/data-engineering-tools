import fs from "fs";
import path from "path";

const LOG_DIR = "./logs";
const LOG_FILE = path.join(LOG_DIR, "bot.log");

function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
  }
}

function timestamp() {
  return new Date().toISOString();
}

/**
 * Escreve em console e em arquivo de log.
 */
function log(level, ...args) {
  const msg = args.map((a) => (typeof a === "object" ? JSON.stringify(a) : String(a))).join(" ");
  const line = `[${timestamp()}] [${level}] ${msg}\n`;
  console[level === "error" ? "error" : "log"](...args);
  try {
    ensureLogDir();
    fs.appendFileSync(LOG_FILE, line);
  } catch (e) {
    console.error("Falha ao escrever log em arquivo:", e.message);
  }
}

export const logger = {
  info: (...args) => log("INFO", ...args),
  warn: (...args) => log("WARN", ...args),
  error: (...args) => log("ERROR", ...args),
};
