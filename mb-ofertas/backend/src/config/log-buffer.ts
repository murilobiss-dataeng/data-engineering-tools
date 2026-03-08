/** Buffer em memória para exibir logs no painel (aba Logs). Útil para o usuário colar erros e para debug. */
const MAX_ENTRIES = 500;

export type LogEntry = {
  id: string;
  at: string;
  level: "info" | "warn" | "error" | "user";
  message: string;
};

const buffer: LogEntry[] = [];
let idCounter = 0;

function nextId(): string {
  return `log-${Date.now()}-${++idCounter}`;
}

export function appendLog(level: LogEntry["level"], message: string): void {
  buffer.push({
    id: nextId(),
    at: new Date().toISOString(),
    level,
    message: message.slice(0, 50_000),
  });
  while (buffer.length > MAX_ENTRIES) buffer.shift();
}

export function getLogs(limit = 200): LogEntry[] {
  return buffer.slice(-limit).reverse();
}
