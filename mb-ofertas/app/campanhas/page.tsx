"use client";

import { useEffect, useState } from "react";
import { api, type Campaign, type Product } from "@/lib/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [sendModal, setSendModal] = useState<Campaign | null>(null);
  const [phones, setPhones] = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    Promise.all([
      api<{ campaigns: Campaign[] }>("/campaigns?limit=50"),
      api<{ products: Product[] }>("/products?status=approved&limit=100"),
    ])
      .then(([c, p]) => {
        setCampaigns(c.campaigns);
        setProducts(p.products);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  async function handleSendNow() {
    if (!sendModal) return;
    const list = phones
      .split(/[\n,;]+/)
      .map((s) => s.replace(/\D/g, "").trim())
      .filter((s) => s.length >= 10);
    if (list.length === 0) {
      alert("Informe ao menos um número (DDD + número).");
      return;
    }
    setSending(true);
    try {
      await api(`/campaigns/${sendModal.id}/send-now`, {
        method: "POST",
        body: JSON.stringify({
          recipientPhones: list.map((n) => (n.startsWith("55") ? n : "55" + n)),
        }),
      });
      alert("Envio enfileirado. As mensagens serão enviadas com delay anti-ban.");
      setSendModal(null);
      setPhones("");
    } catch (e) {
      console.error(e);
      alert("Erro ao enfileirar envio.");
    } finally {
      setSending(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <p className="text-stone-500">Carregando campanhas…</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Campanhas</h1>
          <p className="page-subtitle">Envie ofertas por WhatsApp para sua lista.</p>
        </div>
        <a href="/campanhas/nova" className="btn-primary">
          Nova campanha
        </a>
      </div>

      <ul className="space-y-4">
        {campaigns.length === 0 && (
          <li className="card-flat p-8 text-center text-stone-500">
            Nenhuma campanha. Crie uma e adicione produtos aprovados.
          </li>
        )}
        {campaigns.map((c) => (
          <li key={c.id} className="card flex items-center justify-between p-5">
            <div>
              <p className="font-semibold text-stone-900">{c.name}</p>
              <p className="text-sm text-stone-500">
                Status: {c.status} • {c.product_ids?.length ?? 0} produto(s)
              </p>
            </div>
            <div className="flex gap-2">
              {["draft", "scheduled"].includes(c.status) && (
                <button onClick={() => setSendModal(c)} className="btn-primary text-sm">
                  Enviar agora
                </button>
              )}
              <a href={`/campanhas/${c.id}`} className="btn-secondary text-sm">
                Ver
              </a>
            </div>
          </li>
        ))}
      </ul>

      {sendModal && (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50">
          <div className="card-flat w-full max-w-md p-6 shadow-xl">
            <h3 className="mb-2 font-semibold text-stone-900">Enviar agora: {sendModal.name}</h3>
            <p className="mb-4 text-sm text-stone-600">
              Um número por linha ou separados por vírgula (com DDD, ex: 11999999999)
            </p>
            <textarea
              value={phones}
              onChange={(e) => setPhones(e.target.value)}
              placeholder="11999999999&#10;21988887777"
              rows={5}
              className="input mb-4 w-full"
            />
            <div className="flex justify-end gap-2">
              <button onClick={() => setSendModal(null)} className="btn-secondary">
                Cancelar
              </button>
              <button
                onClick={handleSendNow}
                disabled={sending}
                className="btn-primary disabled:opacity-50"
              >
                {sending ? "Enfileirando..." : "Enviar"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
