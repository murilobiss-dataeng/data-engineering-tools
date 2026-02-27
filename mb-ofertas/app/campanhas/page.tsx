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

  if (loading) return <p className="text-slate-500">Carregando...</p>;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold text-slate-800">Campanhas</h2>
        <a href="/campanhas/nova" className="btn-primary">
          Nova campanha
        </a>
      </div>

      <ul className="space-y-4">
        {campaigns.length === 0 && (
          <li className="card p-8 text-center text-slate-500">
            Nenhuma campanha. Crie uma e adicione produtos aprovados.
          </li>
        )}
        {campaigns.map((c) => (
          <li key={c.id} className="card flex items-center justify-between p-4">
            <div>
              <p className="font-medium">{c.name}</p>
              <p className="text-sm text-slate-500">
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
          <div className="card w-full max-w-md p-6 shadow-xl">
            <h3 className="mb-2 font-semibold">Enviar agora: {sendModal.name}</h3>
            <p className="mb-4 text-sm text-slate-600">
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
