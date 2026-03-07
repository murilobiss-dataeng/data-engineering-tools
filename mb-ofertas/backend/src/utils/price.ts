/**
 * Garante 2 casas decimais para preços (ex.: 386.1 → 386.10).
 */

/** Arredonda valor numérico para exatamente 2 casas decimais (para persistência). */
export function roundToTwoDecimals(value: number): number {
  return Math.round(value * 100) / 100;
}

/** Formata valor (número ou string) como string com exatamente 2 casas decimais (ex.: "386.10"). */
export function toTwoDecimalsString(value: number | string | null | undefined): string | null {
  if (value === null || value === undefined) return null;
  const n = typeof value === "string" ? parseFloat(value) : value;
  if (!Number.isFinite(n)) return null;
  return roundToTwoDecimals(n).toFixed(2);
}
