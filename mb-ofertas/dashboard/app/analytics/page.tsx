"use client";

import { useEffect, useState } from "react";
import { api, type ShortLinkAnalytics } from "@/lib/api";

export default function AnalyticsPage() {
  const [links, setLinks] = useState<ShortLinkAnalytics[]>([]);
  const [totalClicks, setTotalClicks] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api<{ links: ShortLinkAnalytics[]; totalClicks: number }>("/short-links/analytics?limit=200")
      .then((data) => {
        setLinks(data.links);
        setTotalClicks(data.totalClicks);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-slate-500">Carregando...</p>;

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold">Analytics de cliques</h2>
        <p className="mt-2 text-sm text-slate-600">
          Total de cliques rastreados: <strong>{totalClicks}</strong>
        </p>
      </div>

      <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white shadow-sm">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50 text-left text-slate-600">
            <tr>
              <th className="px-4 py-3">Produto</th>
              <th className="px-4 py-3">Categoria</th>
              <th className="px-4 py-3">Link amigável</th>
              <th className="px-4 py-3">Cliques</th>
              <th className="px-4 py-3">Último clique</th>
            </tr>
          </thead>
          <tbody>
            {links.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-center text-slate-500">
                  Nenhum link curto encontrado ainda.
                </td>
              </tr>
            )}
            {links.map((link) => (
              <tr key={link.code} className="border-t border-slate-100">
                <td className="px-4 py-3">
                  <div className="font-medium text-slate-900">{link.product_title || "Sem produto vinculado"}</div>
                  <div className="max-w-xl truncate text-xs text-slate-400">{link.long_url}</div>
                </td>
                <td className="px-4 py-3 uppercase text-slate-600">{link.category_slug || "-"}</td>
                <td className="px-4 py-3 font-mono text-xs text-slate-700">{link.short_url_path}</td>
                <td className="px-4 py-3 font-semibold text-slate-900">{link.click_count}</td>
                <td className="px-4 py-3 text-slate-600">
                  {link.last_clicked_at ? new Date(link.last_clicked_at).toLocaleString("pt-BR") : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
