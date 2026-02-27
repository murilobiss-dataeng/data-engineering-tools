"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, type Product } from "@/lib/api";

export default function ProductDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [product, setProduct] = useState<Product | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [postContent, setPostContent] = useState<{ text: string; imageUrl: string | null } | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api<Product>(`/products/${id}`).then(setProduct).catch(console.error);
  }, [id]);

  useEffect(() => {
    if (!id) return;
    api<{ message: string }>(`/products/${id}/preview-message`)
      .then((d) => setPreview(d.message))
      .catch(console.error);
  }, [id]);

  async function loadPostContent() {
    try {
      const data = await api<{ text: string; imageUrl: string | null }>(`/products/${id}/post-content`);
      setPostContent(data);
    } catch (e) {
      console.error(e);
    }
  }

  async function copyPostText() {
    if (!postContent?.text) return;
    await navigator.clipboard.writeText(postContent.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  if (!product) return <p className="text-slate-500">Carregando…</p>;

  return (
    <div className="space-y-6">
      <a href="/" className="text-sm font-medium text-slate-600 hover:text-slate-900">
        ← Voltar aos produtos
      </a>
      <div className="card">
        <div className="flex flex-col gap-6 sm:flex-row">
          {product.image_url && (
            <img
              src={product.image_url}
              alt=""
              className="h-40 w-40 shrink-0 rounded-lg object-cover"
            />
          )}
          <div className="min-w-0 flex-1">
            <h1 className="text-xl font-semibold text-slate-900">{product.title}</h1>
            <p className="mt-2 text-slate-600">
              R$ {product.price}
              {product.previous_price && (
                <span className="ml-2 text-slate-400 line-through">R$ {product.previous_price}</span>
              )}
              {product.discount_pct && (
                <span className="ml-2 font-medium text-emerald-600">{product.discount_pct}% OFF</span>
              )}
            </p>
            <p className="mt-1 text-sm text-slate-400">Status: {product.status}</p>
            <a
              href={product.affiliate_link}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-block text-sm font-medium text-emerald-600 hover:underline"
            >
              Abrir link de afiliado →
            </a>
          </div>
        </div>
      </div>
      {preview && (
        <div className="card">
          <h2 className="mb-2 font-semibold text-slate-800">Preview da mensagem WhatsApp</h2>
          <pre className="whitespace-pre-wrap rounded-lg bg-slate-50 p-4 text-sm text-slate-700">
            {preview}
          </pre>
        </div>
      )}
      <div className="card">
        <h2 className="mb-2 font-semibold text-slate-800">Conteúdo para post (copiar e colar)</h2>
        <p className="mb-4 text-sm text-slate-600">
          Texto e imagem prontos para você colar em redes sociais ou WhatsApp.
        </p>
        {!postContent ? (
          <button type="button" onClick={loadPostContent} className="btn-primary">
            Gerar conteúdo para post
          </button>
        ) : (
          <div className="space-y-4">
            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm font-medium text-slate-700">Texto</span>
                <button
                  type="button"
                  onClick={copyPostText}
                  className="rounded bg-amber-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-amber-600"
                >
                  {copied ? "Copiado!" : "Copiar texto"}
                </button>
              </div>
              <pre className="max-h-48 overflow-auto rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm whitespace-pre-wrap text-slate-800">
                {postContent.text}
              </pre>
            </div>
            {postContent.imageUrl && (
              <div>
                <span className="mb-2 block text-sm font-medium text-slate-700">Imagem</span>
                <img
                  src={postContent.imageUrl}
                  alt="Produto"
                  className="max-h-64 rounded-lg border border-slate-200 object-contain shadow-sm"
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
