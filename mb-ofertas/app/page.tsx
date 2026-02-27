"use client";

import { useEffect, useState } from "react";
import { api, type Product } from "@/lib/api";

const FILTERS = [
  { value: "", label: "Todos" },
  { value: "pending", label: "Pendentes" },
  { value: "approved", label: "Aprovados" },
  { value: "rejected", label: "Rejeitados" },
] as const;

function StatusBadge({ status }: { status: string }) {
  if (status === "approved") return <span className="badge-approved">Aprovado</span>;
  if (status === "rejected") return <span className="badge-rejected">Rejeitado</span>;
  return <span className="badge-pending">Pendente</span>;
}

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

  if (loading) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <p className="text-stone-500">Carregando produtos…</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Produtos (ofertas)</h1>
          <p className="page-subtitle">
            Cadastre ofertas manualmente ou busque por URL da Amazon/Mercado Livre.
          </p>
        </div>
        <a href="/produtos/novo" className="btn-primary">
          <PlusIcon />
          Nova oferta
        </a>
      </div>

      <div className="mb-6 flex flex-wrap gap-2">
        {FILTERS.map(({ value, label }) => (
          <button
            key={value}
            type="button"
            onClick={() => setFilter(value)}
            className={filter === value ? "tab-active" : "tab"}
          >
            {label}
          </button>
        ))}
      </div>

      <ul className="space-y-4">
        {products.length === 0 && (
          <li className="card-flat flex flex-col items-center justify-center gap-6 py-16 text-center">
            <div className="rounded-full bg-stone-100 p-4">
              <PackageIcon className="h-10 w-10 text-stone-400" />
            </div>
            <div>
              <p className="font-medium text-stone-700">Nenhum produto encontrado</p>
              <p className="mt-1 text-sm text-stone-500">
                Crie sua primeira oferta buscando por URL ou cadastrando manualmente.
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-3">
              <a href="/gerar-oferta" className="btn-primary">
                Buscar por URL (Amazon / ML)
              </a>
              <a href="/produtos/novo" className="btn-secondary">
                Cadastrar manualmente
              </a>
            </div>
          </li>
        )}
        {products.map((p) => (
          <li key={p.id} className="card flex flex-wrap items-center gap-5 p-5">
            <div className="h-24 w-24 shrink-0 overflow-hidden rounded-xl bg-stone-100">
              {p.image_url ? (
                <img src={p.image_url} alt="" className="h-full w-full object-cover" />
              ) : (
                <div className="flex h-full w-full items-center justify-center text-stone-400">
                  <PackageIcon className="h-10 w-10" />
                </div>
              )}
            </div>
            <div className="min-w-0 flex-1">
              <p className="font-semibold text-stone-900 line-clamp-2">{p.title}</p>
              <div className="mt-1.5 flex flex-wrap items-center gap-2">
                <span className="font-semibold text-amber-700">R$ {p.price}</span>
                {p.previous_price && (
                  <span className="text-sm text-stone-400 line-through">R$ {p.previous_price}</span>
                )}
                {p.discount_pct && (
                  <span className="badge bg-amber-100 text-amber-800">{p.discount_pct}% OFF</span>
                )}
              </div>
              <div className="mt-2">
                <StatusBadge status={p.status} />
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {p.status === "pending" && (
                <>
                  <button
                    type="button"
                    onClick={() => updateStatus(p.id, "approved")}
                    className="btn-primary text-sm"
                  >
                    Aprovar
                  </button>
                  <button
                    type="button"
                    onClick={() => updateStatus(p.id, "rejected")}
                    className="btn-secondary text-sm"
                  >
                    Reprovar
                  </button>
                </>
              )}
              <a href={`/produtos/${p.id}`} className="btn-secondary text-sm">
                Ver / Gerar post
              </a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

function PlusIcon() {
  return (
    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
    </svg>
  );
}

function PackageIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
      />
    </svg>
  );
}
