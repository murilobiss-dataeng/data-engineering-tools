"use client";

import { useEffect, useState } from "react";
import { api, type Product, type Category } from "@/lib/api";
import { ProductPriceBlock } from "@/components/ProductPriceBlock";

function StatusBadge({ status }: { status: string }) {
  if (status === "approved") return <span className="badge-approved">Aprovado</span>;
  if (status === "rejected") return <span className="badge-rejected">Rejeitado</span>;
  if (status === "sent") return <span className="rounded bg-stone-200 px-2 py-0.5 text-xs text-stone-700">Enviado</span>;
  return <span className="badge-pending">Pendente</span>;
}

type FetchOfertasResult = { inserted: number; failed: number; totalUrls: number; message: string };

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [categoryFilter, setCategoryFilter] = useState<string>("");
  const [couponDraft, setCouponDraft] = useState<Record<string, string>>({});
  const [fetchOfertasLoading, setFetchOfertasLoading] = useState(false);
  const [fetchOfertasResult, setFetchOfertasResult] = useState<FetchOfertasResult | null>(null);

  const loadProducts = () => {
    const params = new URLSearchParams();
    if (categoryFilter) params.set("categoryId", categoryFilter);
    params.set("limit", "100");
    return api<{ products: Product[] }>(`/products?${params.toString()}`)
      .then((data) => {
        const seen = new Set<string>();
        const unique = data.products.filter((p) => {
          const key = p.affiliate_link;
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });
        setProducts(unique);
        setCouponDraft((prev) => {
          const next = { ...prev };
          for (const p of unique) {
            if (next[p.id] === undefined && p.coupon) next[p.id] = p.coupon;
          }
          return next;
        });
      })
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
  }, [categoryFilter]);

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
      const msg = e instanceof Error ? e.message : "Erro ao atualizar";
      alert(msg);
    }
  }

  /** Rejeitar = apagar o produto do banco. */
  async function rejectProduct(id: string) {
    if (!confirm("Rejeitar e remover esta oferta do sistema?")) return;
    try {
      await api<{ deleted: boolean }>(`/products/${id}`, { method: "DELETE" });
      setProducts((prev) => prev.filter((p) => p.id !== id));
    } catch (e) {
      console.error(e);
      alert("Erro ao remover produto.");
    }
  }

  async function saveCoupon(id: string) {
    const raw = (couponDraft[id] ?? "").trim();
    try {
      const updated = await api<Product>(`/products/${id}/coupon`, {
        method: "PATCH",
        body: JSON.stringify({ coupon: raw || null }),
      });
      setProducts((prev) => prev.map((p) => (p.id === id ? updated : p)));
      setCouponDraft((prev) => ({ ...prev, [id]: updated.coupon ?? "" }));
    } catch (e) {
      console.error(e);
      alert("Erro ao salvar cupom.");
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
            Lista única com todos os produtos. Defina um cupom (opcional) ou rejeite a oferta. Cadastre manualmente ou busque por URL
            da Amazon/Mercado Livre.
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
              <ProductPriceBlock
                variant="compact"
                price={p.price}
                previous_price={p.previous_price}
                discount_pct={p.discount_pct}
                installments={p.installments}
                installment_max_times={p.installment_max_times}
                installment_unit_price={p.installment_unit_price}
              />
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <span className="text-xs text-stone-500">Status:</span>
                <StatusBadge status={p.status} />
                <span className="rounded bg-stone-100 px-2 py-0.5 text-xs text-stone-600">
                  {p.category_name ?? "Sem categoria"}
                </span>
                <span className="text-xs text-stone-400" title={`Origem: ${p.source}`}>
                  {p.source === "amazon" ? "Amazon" : p.source === "mercadolivre" ? "ML" : p.source === "shopee" ? "Shopee" : p.source}
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
              <div className="mt-3 flex max-w-xl flex-wrap items-center gap-2">
                <label className="text-xs font-medium text-stone-600">Cupom</label>
                <input
                  type="text"
                  className="min-w-[10rem] flex-1 rounded-lg border border-stone-200 px-2 py-1.5 text-sm text-stone-800"
                  placeholder="Opcional — aparece na mensagem (WhatsApp)"
                  value={couponDraft[p.id] !== undefined ? couponDraft[p.id] : (p.coupon ?? "")}
                  onChange={(e) => setCouponDraft((prev) => ({ ...prev, [p.id]: e.target.value }))}
                />
                <button type="button" onClick={() => saveCoupon(p.id)} className="btn-secondary text-sm">
                  Salvar cupom
                </button>
              </div>
            </div>
            <div className="flex flex-col gap-2 sm:items-end">
              <div className="flex flex-wrap justify-end gap-2">
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
                    Rejeitar
                  </button>
                </>
              )}
              {p.status === "approved" && (
                <button
                  type="button"
                  onClick={() => rejectProduct(p.id)}
                  className="rounded bg-red-100 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-200"
                >
                  Rejeitar
                </button>
              )}
              <a href={`/produtos/${p.id}`} className="btn-secondary text-sm">
                Ver / Gerar post
              </a>
              </div>
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
