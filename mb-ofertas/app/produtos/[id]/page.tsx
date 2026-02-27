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

  if (!product) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <p className="text-stone-500">Carregando…</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <a href="/" className="btn-ghost text-sm">
        ← Voltar aos produtos
      </a>

      <div className="card-flat">
        <div className="flex flex-col gap-6 sm:flex-row">
          <div className="h-48 w-48 shrink-0 overflow-hidden rounded-xl bg-stone-100">
            {product.image_url ? (
              <img src={product.image_url} alt="" className="h-full w-full object-cover" />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-stone-400">—</div>
            )}
          </div>
          <div className="min-w-0 flex-1">
            <h1 className="text-xl font-bold text-stone-900">{product.title}</h1>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <span className="font-semibold text-amber-700">R$ {product.price}</span>
              {product.previous_price && (
                <span className="text-stone-400 line-through">R$ {product.previous_price}</span>
              )}
              {product.discount_pct && (
                <span className="badge bg-amber-100 text-amber-800">{product.discount_pct}% OFF</span>
              )}
            </div>
            <p className="mt-2 text-sm text-stone-500">Status: {product.status}</p>
            <a
              href={product.affiliate_link}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-block text-sm font-medium text-amber-700 hover:underline"
            >
              Abrir link de afiliado →
            </a>
          </div>
        </div>
      </div>

      {preview && (
        <div className="card-flat">
          <h2 className="mb-2 font-semibold text-stone-800">Preview da mensagem WhatsApp</h2>
          <pre className="whitespace-pre-wrap rounded-xl bg-stone-50 p-4 text-sm text-stone-700">
            {preview}
          </pre>
        </div>
      )}

      <div className="card-flat">
        <h2 className="mb-1 font-semibold text-stone-800">Conteúdo para post</h2>
        <p className="mb-4 text-sm text-stone-500">
          Texto e imagem prontos para copiar e colar em redes sociais ou WhatsApp.
        </p>
        {!postContent ? (
          <button type="button" onClick={loadPostContent} className="btn-primary">
            Gerar conteúdo para post
          </button>
        ) : (
          <div className="space-y-4">
            <div>
              <div className="mb-2 flex items-center justify-between">
                <span className="text-sm font-medium text-stone-700">Texto</span>
                <button
                  type="button"
                  onClick={copyPostText}
                  className="btn-primary text-sm"
                >
                  {copied ? "Copiado!" : "Copiar texto"}
                </button>
              </div>
              <pre className="max-h-48 overflow-auto rounded-xl border border-stone-200 bg-stone-50 p-4 text-sm whitespace-pre-wrap text-stone-800">
                {postContent.text}
              </pre>
            </div>
            {postContent.imageUrl && (
              <div>
                <span className="mb-2 block text-sm font-medium text-stone-700">Imagem</span>
                <img
                  src={postContent.imageUrl}
                  alt="Produto"
                  className="max-h-64 rounded-xl border border-stone-200 object-contain shadow-sm"
                />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
