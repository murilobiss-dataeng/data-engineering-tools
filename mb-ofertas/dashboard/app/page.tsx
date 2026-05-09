"use client";

import { useEffect, useState } from "react";
import { api, type Category, type Product } from "@/lib/api";
import { formatPriceTwoDecimals } from "@/lib/format";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [couponDraft, setCouponDraft] = useState<Record<string, string>>({});

  useEffect(() => {
    Promise.all([
      api<{ products: Product[] }>("/products?limit=200&inQueue=1"),
      api<{ categories: Category[] }>("/categories"),
    ])
      .then(([productsData, categoriesData]) => {
        setProducts(productsData.products);
        setCategories(categoriesData.categories);
        setCouponDraft((prev) => {
          const next = { ...prev };
          for (const p of productsData.products) {
            if (next[p.id] === undefined && p.coupon) next[p.id] = p.coupon;
          }
          return next;
        });
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  async function updateCategory(id: string, categoryId: string | null) {
    try {
      const updated = await api<Product>(`/products/${id}/category`, {
        method: "PATCH",
        body: JSON.stringify({ categoryId }),
      });
      setProducts((prev) => prev.map((p) => (p.id === id ? updated : p)));
    } catch (e) {
      console.error(e);
      alert("Erro ao atualizar categoria.");
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

  async function rejectProduct(id: string) {
    if (!confirm("Tirar esta oferta da fila? O registro permanece no sistema.")) return;
    try {
      await api(`/products/${id}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status: "rejected" }),
      });
      setProducts((prev) => prev.filter((p) => p.id !== id));
    } catch (e) {
      console.error(e);
      alert("Erro ao atualizar oferta.");
    }
  }

  if (loading) return <p className="text-slate-500">Carregando...</p>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Produtos (ofertas)</h2>
          <p className="mt-1 text-sm text-slate-500">
            Fila do painel (não enviadas). Cupom opcional; rejeitar tira da fila e mantém o registro para dedupe.
          </p>
        </div>
      </div>

      <ul className="space-y-4">
        {products.length === 0 && (
          <li className="rounded-lg border border-slate-200 bg-white p-6 text-center text-slate-500">
            Nenhum produto encontrado.
          </li>
        )}
        {products.map((p) => (
          <li
            key={p.id}
            className="flex flex-wrap items-center gap-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
          >
            {p.image_url && (
              <img
                src={p.image_url}
                alt=""
                className="h-20 w-20 rounded object-cover"
              />
            )}
            <div className="min-w-0 flex-1">
              <p className="font-medium text-slate-900">{p.title}</p>
              <p className="text-sm text-slate-600">
                R$ {formatPriceTwoDecimals(p.price)}
                {p.previous_price && (
                  <span className="ml-2 line-through">R$ {formatPriceTwoDecimals(p.previous_price)}</span>
                )}
                {p.discount_pct && (
                  <span className="ml-2 text-green-600">{p.discount_pct}% OFF</span>
                )}
              </p>
              <p className="mt-1 text-xs text-slate-400">
                Status: {p.status} {p.category_slug ? `• Categoria: ${p.category_slug}` : ""}
              </p>
              <select
                value={p.category_id || ""}
                onChange={(e) => updateCategory(p.id, e.target.value || null)}
                className="mt-2 rounded border border-slate-300 px-3 py-1.5 text-sm"
              >
                <option value="">Sem categoria</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
              <div className="mt-2 flex max-w-lg flex-wrap items-center gap-2">
                <label className="text-xs text-slate-600">Cupom</label>
                <input
                  type="text"
                  className="min-w-[8rem] flex-1 rounded border border-slate-300 px-2 py-1 text-sm"
                  placeholder="Opcional"
                  value={couponDraft[p.id] !== undefined ? couponDraft[p.id] : (p.coupon ?? "")}
                  onChange={(e) => setCouponDraft((prev) => ({ ...prev, [p.id]: e.target.value }))}
                />
                <button
                  type="button"
                  onClick={() => saveCoupon(p.id)}
                  className="rounded border border-slate-300 bg-white px-2 py-1 text-xs hover:bg-slate-50"
                >
                  Salvar cupom
                </button>
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => rejectProduct(p.id)}
                className="rounded bg-red-50 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-100"
              >
                Rejeitar
              </button>
              <a
                href={`/produtos/${p.id}`}
                className="rounded border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50"
              >
                Ver
              </a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
