"use client";

import { useEffect, useState } from "react";
import { api, type Category, type Product } from "@/lib/api";
import { formatPriceTwoDecimals } from "@/lib/format";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("pending");

  useEffect(() => {
    Promise.all([
      api<{ products: Product[] }>(`/products?status=${filter}&limit=100`),
      api<{ categories: Category[] }>("/categories"),
    ])
      .then(([productsData, categoriesData]) => {
        setProducts(productsData.products);
        setCategories(categoriesData.categories);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [filter]);

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

  if (loading) return <p className="text-slate-500">Carregando...</p>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Produtos (ofertas)</h2>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm"
        >
          <option value="">Todos</option>
          <option value="pending">Pendentes</option>
          <option value="approved">Aprovados</option>
          <option value="rejected">Rejeitados</option>
        </select>
      </div>

      <ul className="space-y-4">
        {products.length === 0 && (
          <li className="rounded-lg border border-slate-200 bg-white p-6 text-center text-slate-500">
            Nenhum produto encontrado. Rode o pipeline de captura ou cadastre manualmente.
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
            </div>
            <select
              value={p.category_id || ""}
              onChange={(e) => updateCategory(p.id, e.target.value || null)}
              className="rounded border border-slate-300 px-3 py-1.5 text-sm"
            >
              <option value="">Sem categoria</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
            <div className="flex gap-2">
              {p.status === "pending" && (
                <>
                  <button
                    onClick={() => updateStatus(p.id, "approved")}
                    className="rounded bg-green-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-green-700"
                  >
                    Aprovar
                  </button>
                  <button
                    onClick={() => rejectProduct(p.id)}
                    className="rounded bg-slate-200 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-300"
                  >
                    Reprovar
                  </button>
                </>
              )}
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
