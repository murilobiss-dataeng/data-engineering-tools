"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type Product } from "@/lib/api";
import { parseInstallmentParts } from "@/lib/installments";

export default function NovoProdutoPage() {
  const router = useRouter();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    title: "",
    price: "",
    previousPrice: "",
    affiliateLink: "",
    imageUrl: "",
    installments: "",
    installmentMaxTimes: "",
    installmentUnitPrice: "",
  });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    const price = form.price ? parseFloat(form.price.replace(",", ".")) : NaN;
    const previousPrice = form.previousPrice ? parseFloat(form.previousPrice.replace(",", ".")) : null;
    if (!form.title.trim()) {
      setError("Título é obrigatório.");
      return;
    }
    if (!Number.isFinite(price) || price <= 0) {
      setError("Preço deve ser um valor maior que zero.");
      return;
    }
    if (!form.affiliateLink.trim()) {
      setError("Link de afiliado é obrigatório.");
      return;
    }
    const instMax = form.installmentMaxTimes.trim()
      ? parseInt(form.installmentMaxTimes.trim(), 10)
      : NaN;
    const instUnit = form.installmentUnitPrice.trim()
      ? parseFloat(form.installmentUnitPrice.replace(",", "."))
      : NaN;
    let maxT = Number.isFinite(instMax) && instMax > 0 ? instMax : null;
    let unitP = Number.isFinite(instUnit) && instUnit > 0 ? instUnit : null;
    if ((maxT == null || unitP == null) && form.installments.trim()) {
      const p = parseInstallmentParts(form.installments);
      if (p.maxTimes && p.unitPrice) {
        maxT = p.maxTimes;
        unitP = p.unitPrice;
      }
    }

    setSaving(true);
    try {
      const product = await api<Product>("/products", {
        method: "POST",
        body: JSON.stringify({
          title: form.title.trim(),
          price,
          previousPrice: previousPrice && Number.isFinite(previousPrice) ? previousPrice : null,
          affiliateLink: form.affiliateLink.trim(),
          imageUrl: form.imageUrl.trim() || null,
          installments: form.installments.trim() || undefined,
          installmentMaxTimes: maxT ?? undefined,
          installmentUnitPrice: unitP ?? undefined,
          source: "manual",
        }),
      });
      router.push(`/produtos/${product.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao salvar.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div>
      <a href="/" className="btn-ghost mb-6 text-sm">
        ← Voltar aos produtos
      </a>
      <div className="mb-8">
        <h1 className="page-title">Nova oferta</h1>
        <p className="page-subtitle">
          Cadastre um produto manualmente. Ele entra na fila do painel; depois você pode gerar o conteúdo para post.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="card-flat max-w-2xl space-y-6">
        <div>
          <label htmlFor="title" className="input-label">
            Título do produto *
          </label>
          <input
            id="title"
            type="text"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            placeholder="Ex.: Fone Bluetooth XYZ"
            className="input"
            required
          />
        </div>

        <div className="grid gap-6 sm:grid-cols-2">
          <div>
            <label htmlFor="price" className="input-label">
              À vista (R$) *
            </label>
            <input
              id="price"
              type="text"
              inputMode="decimal"
              value={form.price}
              onChange={(e) => setForm({ ...form, price: e.target.value })}
              placeholder="99,90"
              className="input"
              required
            />
          </div>
          <div>
            <label htmlFor="previousPrice" className="input-label">
              Preço cheio (R$) — opcional
            </label>
            <input
              id="previousPrice"
              type="text"
              inputMode="decimal"
              value={form.previousPrice}
              onChange={(e) => setForm({ ...form, previousPrice: e.target.value })}
              placeholder="129,90"
              className="input"
            />
          </div>
        </div>

        <div className="grid gap-6 sm:grid-cols-3">
          <div className="sm:col-span-3">
            <label htmlFor="installments" className="input-label">
              Parcelamento — texto (opcional)
            </label>
            <input
              id="installments"
              type="text"
              value={form.installments}
              onChange={(e) => setForm({ ...form, installments: e.target.value })}
              placeholder="ex.: em 12x de R$ 25,00 sem juros"
              className="input"
            />
          </div>
          <div>
            <label htmlFor="installmentMaxTimes" className="input-label">
              Até quantas vezes
            </label>
            <input
              id="installmentMaxTimes"
              type="text"
              inputMode="numeric"
              value={form.installmentMaxTimes}
              onChange={(e) => setForm({ ...form, installmentMaxTimes: e.target.value })}
              placeholder="12"
              className="input"
            />
          </div>
          <div>
            <label htmlFor="installmentUnitPrice" className="input-label">
              Valor da parcela (R$)
            </label>
            <input
              id="installmentUnitPrice"
              type="text"
              inputMode="decimal"
              value={form.installmentUnitPrice}
              onChange={(e) => setForm({ ...form, installmentUnitPrice: e.target.value })}
              placeholder="25,90"
              className="input"
            />
          </div>
        </div>

        <div>
          <label htmlFor="affiliateLink" className="input-label">
            Link de afiliado *
          </label>
          <input
            id="affiliateLink"
            type="url"
            value={form.affiliateLink}
            onChange={(e) => setForm({ ...form, affiliateLink: e.target.value })}
            placeholder="https://..."
            className="input"
            required
          />
        </div>

        <div>
          <label htmlFor="imageUrl" className="input-label">
            URL da imagem — opcional
          </label>
          <input
            id="imageUrl"
            type="url"
            value={form.imageUrl}
            onChange={(e) => setForm({ ...form, imageUrl: e.target.value })}
            placeholder="https://..."
            className="input"
          />
          {form.imageUrl && (
            <img
              src={form.imageUrl}
              alt="Preview"
              className="mt-2 h-24 w-24 rounded-lg border border-stone-200 object-cover"
            />
          )}
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <div className="flex flex-wrap gap-3 pt-2">
          <button type="submit" disabled={saving} className="btn-primary">
            {saving ? "Salvando…" : "Salvar oferta"}
          </button>
          <a href="/" className="btn-secondary">
            Cancelar
          </a>
        </div>
      </form>
    </div>
  );
}
