/** Igual ao backend: extrai Nx e valor da parcela do texto da loja. */
export function parseInstallmentParts(text: string | null | undefined): {
  maxTimes: number | null;
  unitPrice: number | null;
} {
  if (!text?.trim()) return { maxTimes: null, unitPrice: null };
  const t = text.replace(/\s+/g, " ");
  const m = t.match(/(\d+)\s*x\s*(?:de\s*)?R\$\s*([\d.,]+)/i);
  if (!m) return { maxTimes: null, unitPrice: null };
  const maxTimes = parseInt(m[1], 10);
  const raw = m[2].replace(/\./g, "").replace(",", ".");
  const unitPrice = parseFloat(raw);
  if (!Number.isFinite(maxTimes) || maxTimes < 1 || maxTimes > 48) return { maxTimes: null, unitPrice: null };
  if (!Number.isFinite(unitPrice) || unitPrice <= 0 || unitPrice > 1_000_000) {
    return { maxTimes: null, unitPrice: null };
  }
  return { maxTimes, unitPrice: Math.round(unitPrice * 100) / 100 };
}
