"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, type Product, type Category } from "@/lib/api";

export default function NewCampaignPage() {
  const router = useRouter();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [name, setName] = useState("");
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    Promise.all([
      api<{ products: Product[] }>("/products?status=approved&limit=200"),
      api<{ categories: Category[] }>("/categories"),
    ])
      .then(([p, c]) => {
        setProducts(p.products);
        setCategories(c.categories);
      })
      .catch(console.error);
  }, []);

  function toggle(id: string) {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || selectedIds.size === 0) {
      alert("Preencha o nome e selecione ao menos um produto.");
      return;
    }
    setSubmitting(true);
    try {
      await api("/campaigns", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          productIds: Array.from(selectedIds),
          targetType: "list",
        }),
      });
      router.push("/campanhas");
    } catch (e) {
      console.error(e);
      alert("Erro ao criar campanha.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <a href="/campanhas" className="text-sm text-slate-600 hover:underline">
        ← Voltar
      </a>
      <h2 className="mt-4 text-xl font-semibold">Nova campanha</h2>
      <form onSubmit={handleSubmit} className="mt-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700">Nome da campanha</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 w-full max-w-md rounded border border-slate-300 px-3 py-2"
            placeholder="Ex: Ofertas Black Friday"
          />
        </div>
        <div>
          <p className="text-sm font-medium text-slate-700">
            Produtos aprovados ({selectedIds.size} selecionados)
          </p>
          <ul className="mt-2 max-h-96 space-y-2 overflow-y-auto rounded border border-slate-200 bg-white p-2">
            {products.length === 0 && (
              <li className="py-4 text-center text-slate-500">
                Nenhum produto aprovado. Aprove produtos na lista de Produtos.
              </li>
            )}
            {products.map((p) => (
              <li key={p.id} className="flex items-center gap-3 rounded p-2 hover:bg-slate-50">
                <input
                  type="checkbox"
                  checked={selectedIds.has(p.id)}
                  onChange={() => toggle(p.id)}
                  className="h-4 w-4"
                />
                <span className="flex-1 truncate text-sm">{p.title}</span>
                <span className="text-sm text-slate-500">R$ {p.price}</span>
              </li>
            ))}
          </ul>
        </div>
        <button
          type="submit"
          disabled={submitting || selectedIds.size === 0}
          className="rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
        >
          {submitting ? "Criando..." : "Criar campanha"}
        </button>
      </form>
    </div>
  );
}
