"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api, type Product } from "@/lib/api";

export default function ProductDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [product, setProduct] = useState<Product | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    api<Product>(`/products/${id}`).then(setProduct).catch(console.error);
  }, [id]);

  useEffect(() => {
    if (!id) return;
    api<{ message: string }>(`/products/${id}/preview-message`)
      .then((d) => setPreview(d.message))
      .catch(console.error);
  }, [id]);

  if (!product) return <p className="text-slate-500">Carregando...</p>;

  return (
    <div className="space-y-6">
      <a href="/" className="text-sm text-slate-600 hover:underline">
        ← Voltar
      </a>
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex gap-6">
          {product.image_url && (
            <img
              src={product.image_url}
              alt=""
              className="h-40 w-40 rounded object-cover"
            />
          )}
          <div className="flex-1">
            <h1 className="text-lg font-semibold">{product.title}</h1>
            <p className="mt-2 text-slate-600">
              R$ {product.price}
              {product.previous_price && (
                <span className="ml-2 line-through">R$ {product.previous_price}</span>
              )}
              {product.discount_pct && (
                <span className="ml-2 text-green-600">{product.discount_pct}% OFF</span>
              )}
            </p>
            <p className="mt-1 text-sm text-slate-400">Status: {product.status}</p>
            <a
              href={product.affiliate_link}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-block text-sm text-blue-600 hover:underline"
            >
              Abrir link de afiliado →
            </a>
          </div>
        </div>
      </div>
      {preview && (
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-2 font-semibold">Preview da mensagem WhatsApp</h2>
          <pre className="whitespace-pre-wrap rounded bg-slate-100 p-4 text-sm">
            {preview}
          </pre>
        </div>
      )}
    </div>
  );
}
