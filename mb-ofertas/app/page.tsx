"use client";

import { useEffect, useState } from "react";
import { api, type Product, type Category } from "@/lib/api";

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

type FetchOfertasResult = { inserted: number; failed: number; totalUrls: number; message: string };

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("pending");
  const [categoryFilter, setCategoryFilter] = useState<string>("");
  const [fetchOfertasLoading, setFetchOfertasLoading] = useState(false);
  const [fetchOfertasResult, setFetchOfertasResult] = useState<FetchOfertasResult | null>(null);

  const loadProducts = () => {
    const params = new URLSearchParams();
    if (filter) params.set("status", filter);
    if (categoryFilter) params.set("categoryId", categoryFilter);
    params.set("limit", "50");
    return api<{ products: Product[] }>(`/products?${params.toString()}`)
      .then((data) => setProducts(data.products))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    api<{ categories: Category[] }>("/categories")
      .then((d) => setCategories(d.categories))
      .catch(console.error);
  }, []);

  useEffect(() => {
    setLoading(true);
    loadProducts();
  }, [filter, categoryFilter]);

  async function handleFetchOfertas() {
    setFetchOfertasResult(null);
    setFetchOfertasLoading(true);
    try {
      const result = await api<FetchOfertasResult>("/products/fetch-ofertas", {
        method: "POST",
        body: JSON.stringify({}),
      });
      setFetchOfertasResult(result);
      await loadProducts();
    } catch (e) {
      setFetchOfertasResult({
        inserted: 0,
        failed: 0,
        totalUrls: 0,
        message: e instanceof Error ? e.message : "Erro ao buscar ofertas.",
      });
    } finally {
      setFetchOfertasLoading(false);
    }
  }

  async function updateStatus(id: string, status: "approved") {
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

  /** Reprovar = apagar o produto do banco e tirar da lista. */
  async function rejectProduct(id: string) {
    if (!confirm("Tirar este produto da lista? Ele será apagado do banco.")) return;
    try {
      await api<{ deleted: boolean }>(`/products/${id}`, { method: "DELETE" });
      setProducts((prev) => prev.filter((p) => p.id !== id));
    } catch (e) {
      console.error(e);
      alert("Erro ao remover produto.");
    }
  }

  async function updateProductCategory(id: string, categoryId: string | null) {
    try {
      const updated = await api<Product>(`/products/${id}/category`, {
        method: "PATCH",
        body: JSON.stringify({ categoryId }),
      });
      setProducts((prev) =>
        prev.map((p) =>
          p.id === id
            ? {
                ...p,
                category_id: updated.category_id,
                category_name: updated.category_name,
                category_slug: updated.category_slug,
              }
            : p
        )
      );
    } catch (e) {
      console.error(e);
      alert("Erro ao atualizar categoria.");
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

      <div className="card-flat mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="font-semibold text-stone-800">Buscar ofertas automaticamente</h2>
          <p className="text-sm text-stone-500">
            Usa as URLs configuradas no backend (Amazon e Mercado Livre) e adiciona produtos como pendentes.
          </p>
        </div>
        <div className="flex flex-col gap-2">
          <button
            type="button"
            onClick={handleFetchOfertas}
            disabled={fetchOfertasLoading}
            className="btn-primary"
          >
            {fetchOfertasLoading ? "Buscando… (pode levar 1–2 min)" : "Iniciar busca"}
          </button>
          {fetchOfertasResult && (
            <p className="text-sm text-stone-600">
              {fetchOfertasResult.message}
              {fetchOfertasResult.failed > 0 && ` ${fetchOfertasResult.failed} falha(s).`}
            </p>
          )}
        </div>
      </div>

      <div className="mb-6 flex flex-wrap items-center gap-4">
        <div className="flex flex-wrap gap-2">
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
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium text-stone-600">Categoria:</label>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="rounded-lg border border-stone-300 bg-white px-3 py-1.5 text-sm text-stone-800"
          >
            <option value="">Todas</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
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
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <StatusBadge status={p.status} />
                <span className="rounded bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                  {p.category_name ?? "Sem categoria"}
                </span>
              </div>
              <div className="mt-2">
                <label className="mr-2 text-xs text-stone-500">Categoria (canal):</label>
                <select
                  value={p.category_id ?? ""}
                  onChange={(e) =>
                    updateProductCategory(p.id, e.target.value ? e.target.value : null)
                  }
                  className="rounded border border-stone-200 bg-white px-2 py-1 text-xs text-stone-700"
                >
                  <option value="">Sem categoria</option>
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
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
                    onClick={() => rejectProduct(p.id)}
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
