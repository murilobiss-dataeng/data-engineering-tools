#!/usr/bin/env python3
"""
Gera stores/salmo_dia/data/salmos.ts a partir de data/salmos_completos.py.
Execute na raiz do repositório youtube-content-automation:
  python3 scripts/generate_salmos_store_ts.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data"))
from salmos_completos import SALMOS_COMPLETOS  # noqa: E402

MOOD_PT = {
    "peace": "Paz e confiança",
    "protection": "Proteção",
    "hope": "Esperança",
    "praise": "Louvor",
    "gratitude": "Gratidão",
    "trust": "Confiança",
    "repentance": "Arrependimento",
    "forgiveness": "Perdão",
    "wisdom": "Sabedoria",
    "cry": "Súplica",
    "strength": "Força",
    "night": "Vigília",
    "unity": "União",
    "creation": "Criação",
}


def main() -> None:
    lines: list[str] = []
    lines.append("// Gerado por: python3 scripts/generate_salmos_store_ts.py")
    lines.append("")
    lines.append("export interface Salmo {")
    lines.append("  id: string;")
    lines.append("  slug: string;")
    lines.append("  titulo: string;")
    lines.append("  numero: number;")
    lines.append("  texto: string;")
    lines.append("  tema: string;")
    lines.append("  dataPublicacao: string;")
    lines.append("}")
    lines.append("")
    lines.append(
        "/** Salmos em português (Almeida Corrigida Fiel). Lista sincronizada com data/salmos_completos.py. */"
    )
    lines.append("export const salmos: Salmo[] = [")

    for i, (nome, texto, mood) in enumerate(SALMOS_COMPLETOS):
        num = int(nome.replace("Salmo ", "").strip())
        m = MOOD_PT.get(mood, mood)
        first = texto.strip().split("\n")[0].strip()
        if len(first) > 60:
            first = first[:57] + "…"
        slug = f"salmo-{num}"
        data_pub = f"2025-{((i % 12) + 1):02d}-{((i % 28) + 1):02d}"
        lines.append("  {")
        lines.append(f'    id: "{i + 1}",')
        lines.append(f'    slug: "{slug}",')
        lines.append(f'    titulo: {json.dumps(first, ensure_ascii=False)},')
        lines.append(f"    numero: {num},")
        lines.append(f'    tema: {json.dumps(m, ensure_ascii=False)},')
        lines.append(f'    dataPublicacao: "{data_pub}",')
        safe = texto.strip().replace("`", "\\`").replace("${", "\\${")
        lines.append(f"    texto: `{safe}`,")
        lines.append("  },")

    lines.append("];")
    lines.append("")
    lines.append("export function getSalmoBySlug(slug: string): Salmo | undefined {")
    lines.append("  return salmos.find((s) => s.slug === slug);")
    lines.append("}")
    lines.append("")
    lines.append("export function getSalmosRecentes(limit = 5): Salmo[] {")
    lines.append("  return [...salmos]")
    lines.append("    .sort((a, b) => b.dataPublicacao.localeCompare(a.dataPublicacao))")
    lines.append("    .slice(0, limit);")
    lines.append("}")
    lines.append("")
    lines.append("/** Índice do dia (1..365/366) estável por data UTC. */")
    lines.append("function dayIndexUtc(): number {")
    lines.append("  const d = new Date();")
    lines.append("  const start = Date.UTC(d.getUTCFullYear(), 0, 0);")
    lines.append("  const now = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());")
    lines.append("  return Math.floor((now - start) / 86400000);")
    lines.append("}")
    lines.append("")
    lines.append("/** Salmo do dia: alterna entre todos os salmos (muda a cada dia, fuso UTC). */")
    lines.append("export function getSalmoDoDia(): Salmo {")
    lines.append("  const d = dayIndexUtc();")
    lines.append("  return salmos[d % salmos.length]!;")
    lines.append("}")

    out = ROOT / "stores/salmo_dia/data/salmos.ts"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: {out} ({len(SALMOS_COMPLETOS)} salmos)")


if __name__ == "__main__":
    main()
