"use client";

import { useEffect, useState } from "react";
import { api, type ShortLinkAnalytics } from "@/lib/api";

function shortLinkFullUrl(path: string, origin: string): string {
  const p = path.startsWith("/") ? path : `/${path}`;
  return origin ? `${origin.replace(/\/$/, "")}${p}` : p;
}

export default function AnalyticsPage() {
  const [links, setLinks] = useState<ShortLinkAnalytics[]>([]);
  const [totalClicks, setTotalClicks] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [origin, setOrigin] = useState("");

  useEffect(() => {
    setOrigin(typeof window !== "undefined" ? window.location.origin : "");
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    api<{ links: ShortLinkAnalytics[]; totalClicks: number }>("/short-links/analytics?limit=200")
      .then((data) => {
        setLinks(data.links);
        setTotalClicks(data.totalClicks);
      })
      .catch((e) => {
        console.error(e);
        setError(e instanceof Error ? e.message : "Não foi possível carregar os dados.");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <p className="text-stone-500">Carregando métricas…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card-flat border border-amber-200 bg-amber-50 p-6 text-amber-900">
        <p className="font-medium">Erro ao carregar analytics</p>
        <p className="mt-1 text-sm">{error}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header mb-8">
        <div>
          <h1 className="page-title">Analytics de cliques</h1>
          <p className="page-subtitle">
            Links encurtados gerados pelo painel e quantidade de cliques (redirect <code className="rounded bg-stone-100 px-1">/r/[código]</code>
            ).
          </p>
        </div>
      </div>

      <div className="card-flat mb-6 p-6">
        <p className="text-stone-700">
          Total de cliques rastreados: <strong className="text-stone-900">{totalClicks}</strong>
        </p>
        <p className="mt-2 text-sm text-stone-500">
          Cada clique em um link curto incrementa o contador. O produto aparece quando o link longo coincide com o cadastro.
        </p>
      </div>

      <div className="card-flat overflow-x-auto p-0">
        <table className="min-w-full text-sm">
          <thead className="border-b border-stone-200 bg-stone-50 text-left text-stone-600">
            <tr>
              <th className="px-4 py-3 font-medium">Produto</th>
              <th className="px-4 py-3 font-medium">Categoria</th>
              <th className="px-4 py-3 font-medium">Link curto</th>
              <th className="px-4 py-3 font-medium">Cliques</th>
              <th className="px-4 py-3 font-medium">Último clique</th>
            </tr>
          </thead>
          <tbody>
            {links.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-stone-500">
                  Nenhum link curto registrado ainda. Os links são criados ao gerar mensagens com encurtamento.
                </td>
              </tr>
            )}
            {links.map((link) => {
              const full = shortLinkFullUrl(link.short_url_path || `/r/${link.code}`, origin);
              return (
                <tr key={link.code} className="border-t border-stone-100">
                  <td className="px-4 py-3 align-top">
                    <div className="font-medium text-stone-900">{link.product_title || "Sem produto vinculado"}</div>
                    <div className="font-mono max-w-md truncate text-xs text-stone-400" title={link.long_url}>
                      {link.long_url}
                    </div>
                  </td>
                  <td className="px-4 py-3 uppercase text-stone-600">{link.category_slug || "—"}</td>
                  <td className="px-4 py-3 align-top">
                    <a
                      href={full}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-mono text-xs break-all text-amber-800 underline decoration-amber-300 hover:text-amber-950"
                    >
                      {full}
                    </a>
                  </td>
                  <td className="px-4 py-3 font-semibold text-stone-900">{link.click_count}</td>
                  <td className="px-4 py-3 text-stone-600">
                    {link.last_clicked_at ? new Date(link.last_clicked_at).toLocaleString("pt-BR") : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
