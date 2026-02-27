"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, type ScrapedProduct, type Product } from "@/lib/api";

export default function GerarOfertaPage() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [product, setProduct] = useState<ScrapedProduct | null>(null);
  const [postText, setPostText] = useState<string | null>(null);
  const [postImageUrl, setPostImageUrl] = useState<string | null>(null);
  const [copiedText, setCopiedText] = useState(false);
  const [copiedImage, setCopiedImage] = useState(false);

  async function handleBuscar() {
    if (!url.trim()) {
      setError("Cole a URL do produto (ex.: Amazon).");
      return;
    }
    setError(null);
    setProduct(null);
    setPostText(null);
    setPostImageUrl(null);
    setLoading(true);
    try {
      const data = await api<ScrapedProduct>("/products/from-url", {
        method: "POST",
        body: JSON.stringify({ url: url.trim() }),
      });
      setProduct(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erro ao buscar oferta. Verifique a URL e tente de novo.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGerarConteudo() {
    if (!product) return;
    setError(null);
    try {
      const data = await api<{ text: string; imageUrl: string | null }>("/products/post-content", {
        method: "POST",
        body: JSON.stringify({
          title: product.title,
          price: product.price,
          previousPrice: product.previousPrice,
          discountPct: product.discountPct,
          affiliateLink: product.affiliateLink,
          imageUrl: product.imageUrl,
        }),
      });
      setPostText(data.text);
      setPostImageUrl(data.imageUrl);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erro ao gerar conteúdo.");
    }
  }

  async function copyText() {
    if (!postText) return;
    await navigator.clipboard.writeText(postText);
    setCopiedText(true);
    setTimeout(() => setCopiedText(false), 2000);
  }

  async function copyImageUrl() {
    if (!postImageUrl) return;
    await navigator.clipboard.writeText(postImageUrl);
    setCopiedImage(true);
    setTimeout(() => setCopiedImage(false), 2000);
  }

  async function handleSalvarOferta() {
    if (!product) return;
    setError(null);
    setSaving(true);
    try {
      const saved = await api<Product>("/products", {
        method: "POST",
        body: JSON.stringify({
          title: product.title,
          price: product.price,
          previousPrice: product.previousPrice,
          discountPct: product.discountPct,
          affiliateLink: product.affiliateLink,
          imageUrl: product.imageUrl,
          source: "amazon",
        }),
      });
      router.push(`/produtos/${saved.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erro ao salvar.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="page-title">Buscar oferta por URL</h1>
        <p className="page-subtitle">
          Cole a URL do produto (Amazon ou Mercado Livre) e gere o texto + imagem para copiar e postar.
        </p>
      </div>

      <section className="card-flat">
        <h2 className="text-lg font-semibold text-stone-800">1. Buscar oferta</h2>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-end">
          <div className="flex-1">
            <label className="mb-1 block text-sm font-medium text-slate-700">URL do produto</label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.amazon.com.br/dp/... ou https://www.mercadolivre.com.br/..."
              className="input w-full"
            />
          </div>
          <button
            type="button"
            onClick={handleBuscar}
            disabled={loading}
            className="btn-primary shrink-0"
          >
            {loading ? "Buscando…" : "Buscar oferta"}
          </button>
        </div>
        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      </section>

      {product && (
        <>
<section className="card-flat">
        <h2 className="text-lg font-semibold text-stone-800">2. Dados do produto (edite se quiser)</h2>
            <div className="mt-4 flex flex-col gap-4 sm:flex-row">
              {product.imageUrl && (
                <img
                  src={product.imageUrl}
                  alt=""
                  className="h-36 w-36 shrink-0 rounded-lg border border-slate-200 object-cover"
                />
              )}
              <div className="min-w-0 flex-1 space-y-3">
                <div>
                  <label className="input-label">Título</label>
                  <input
                    type="text"
                    value={product.title}
                    onChange={(e) => setProduct({ ...product, title: e.target.value })}
                    className="input w-full"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                  <div>
                    <label className="input-label">Preço (R$)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={product.price}
                      onChange={(e) => setProduct({ ...product, price: parseFloat(e.target.value) || 0 })}
                      className="input w-full"
                    />
                  </div>
                  <div>
                    <label className="input-label">De (R$) — opcional</label>
                    <input
                      type="number"
                      step="0.01"
                      value={product.previousPrice ?? ""}
                      onChange={(e) =>
                        setProduct({
                          ...product,
                          previousPrice: e.target.value ? parseFloat(e.target.value) : null,
                          discountPct:
                            e.target.value && product.price
                              ? Math.round(
                                  ((parseFloat(e.target.value) - product.price) / parseFloat(e.target.value)) * 100
                                )
                              : null,
                        })
                      }
                      placeholder="—"
                      className="input w-full"
                    />
                  </div>
                  <div>
                    <label className="input-label">Link de afiliado</label>
                    <input
                      type="url"
                      value={product.affiliateLink}
                      onChange={(e) => setProduct({ ...product, affiliateLink: e.target.value })}
                      className="input w-full"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-4 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={handleSalvarOferta}
                disabled={saving}
                className="btn-secondary"
              >
                {saving ? "Salvando…" : "Salvar oferta na lista"}
              </button>
              <span className="text-sm text-stone-500">Salve para aprovar e usar em campanhas.</span>
            </div>
          </section>

          <section className="card-flat">
            <h2 className="text-lg font-semibold text-stone-800">3. Conteúdo para postar</h2>
            <p className="mt-1 text-sm text-stone-600">
              Gere o texto e use a imagem abaixo. Copie e cole onde for postar (WhatsApp, redes sociais, etc.).
            </p>
            <button
              type="button"
              onClick={handleGerarConteudo}
              className="btn-primary mt-4"
            >
              Gerar conteúdo para post
            </button>

            {postText != null && (
              <div className="mt-6 space-y-4">
                <div>
                  <div className="mb-2 flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-700">Texto (copie e cole)</span>
                    <button
                      type="button"
                      onClick={copyText}
                      className="btn-primary text-sm"
                    >
                      {copiedText ? "Copiado!" : "Copiar texto"}
                    </button>
                  </div>
                  <pre className="max-h-48 overflow-auto rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm whitespace-pre-wrap text-slate-800">
                    {postText}
                  </pre>
                </div>
                {postImageUrl && (
                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <span className="text-sm font-medium text-slate-700">Imagem do produto</span>
                      <button
                        type="button"
                        onClick={copyImageUrl}
                        className="btn-secondary text-sm"
                      >
                        {copiedImage ? "Copiado!" : "Copiar URL da imagem"}
                      </button>
                    </div>
                    <div className="flex flex-wrap items-start gap-4">
                      <img
                        src={postImageUrl}
                        alt="Produto"
                        className="max-h-64 rounded-lg border border-slate-200 object-contain shadow-sm"
                      />
                      <p className="text-xs text-slate-500">
                        Use esta imagem no post. Você pode baixar pela URL ou arrastar para o editor.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
