"use client";

import { useEffect, useState } from "react";
import { api, type Product } from "@/lib/api";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("pending");

  useEffect(() => {
    api<{ products: Product[] }>(`/products?status=${filter}&limit=50`)
      .then((data) => setProducts(data.products))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filter]);

  async function updateStatus(id: string, status: "approved" | "rejected") {
    try {
      await api(`/products/${id}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status }),
      });
      setProducts((prev) => prev.map((p) => (p.id === id ? { ...p, status } : p)));
    } catch (e) {
      console.error(e);
      alert("Erro ao atualizar");
    }
  }

  if (loading) return <p className="text-slate-500">Carregando produtos…</p>;

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <h2 className="text-xl font-semibold text-slate-800">Produtos (ofertas)</h2>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="input w-auto min-w-[140px]"
        >
          <option value="">Todos</option>
          <option value="pending">Pendentes</option>
          <option value="approved">Aprovados</option>
          <option value="rejected">Rejeitados</option>
        </select>
      </div>

      <ul className="space-y-4">
        {products.length === 0 && (
          <li className="card p-8 text-center text-slate-500">
            Nenhum produto encontrado. Use <a href="/gerar-oferta" className="text-emerald-600 hover:underline">Gerar oferta</a> para buscar na Amazon ou cadastre manualmente.
          </li>
        )}
        {products.map((p) => (
          <li key={p.id} className="card flex flex-wrap items-center gap-4 p-4">
            {p.image_url && (
              <img src={p.image_url} alt="" className="h-20 w-20 shrink-0 rounded-lg object-cover" />
            )}
            <div className="min-w-0 flex-1">
              <p className="font-medium text-slate-900">{p.title}</p>
              <p className="text-sm text-slate-600">
                R$ {p.price}
                {p.previous_price && (
                  <span className="ml-2 text-slate-400 line-through">R$ {p.previous_price}</span>
                )}
                {p.discount_pct && (
                  <span className="ml-2 font-medium text-emerald-600">{p.discount_pct}% OFF</span>
                )}
              </p>
              <p className="mt-1 text-xs text-slate-400">Status: {p.status}</p>
            </div>
            <div className="flex gap-2">
              {p.status === "pending" && (
                <>
                  <button
                    onClick={() => updateStatus(p.id, "approved")}
                    className="btn-primary text-sm"
                  >
                    Aprovar
                  </button>
                  <button
                    onClick={() => updateStatus(p.id, "rejected")}
                    className="btn-secondary text-sm"
                  >
                    Reprovar
                  </button>
                </>
              )}
              <a href={`/produtos/${p.id}`} className="btn-secondary text-sm">
                Ver
              </a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
