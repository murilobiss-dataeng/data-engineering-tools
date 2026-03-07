"use client";

import { useEffect, useState } from "react";
import { api, type WhatsAppChannel } from "@/lib/api";

export default function CanaisWhatsAppPage() {
  const [channels, setChannels] = useState<WhatsAppChannel[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [channelLink, setChannelLink] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api<{ channels: WhatsAppChannel[] }>("/whatsapp/channels")
      .then((d) => setChannels(d.channels))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    const link = channelLink.trim() || null;
    const num = phone.trim() || null;
    if (!name.trim()) {
      alert("Preencha o nome do canal.");
      return;
    }
    if (!num && !link) {
      alert("Preencha o número ou o link do canal (ex.: canal público mb.OFERTAS).");
      return;
    }
    setSubmitting(true);
    try {
      const created = await api<WhatsAppChannel>("/whatsapp/channels", {
        method: "POST",
        body: JSON.stringify({ name: name.trim(), phone: num ?? "", channelLink: link }),
      });
      setChannels((prev) => [...prev, created]);
      setName("");
      setPhone("");
      setChannelLink("");
    } catch (err) {
      console.error(err);
      alert("Erro ao adicionar canal.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Remover este canal?")) return;
    try {
      await api(`/whatsapp/channels/${id}`, { method: "DELETE" });
      setChannels((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      console.error(err);
      alert("Erro ao remover.");
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <p className="text-stone-500">Carregando…</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Canais WhatsApp</h1>
          <p className="page-subtitle">
            Cadastre os canais (números ou grupos) para o botão &quot;Enviar para o WhatsApp&quot; nas campanhas.
          </p>
        </div>
      </div>

      <div className="card-flat mb-8 p-6">
        <h2 className="mb-4 font-semibold text-stone-800">Adicionar canal</h2>
        <form onSubmit={handleAdd} className="flex flex-wrap items-end gap-4">
          <div className="min-w-[200px]">
            <label className="mb-1 block text-sm font-medium text-stone-600">Nome do canal</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Ex: Ofertas Casa"
              className="input w-full"
            />
          </div>
          <div className="min-w-[180px]">
            <label className="mb-1 block text-sm font-medium text-stone-600">Número (opcional)</label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="11999999999"
              className="input w-full"
            />
          </div>
          <div className="min-w-[280px]">
            <label className="mb-1 block text-sm font-medium text-stone-600">Link do canal (opcional)</label>
            <input
              type="url"
              value={channelLink}
              onChange={(e) => setChannelLink(e.target.value)}
              placeholder="https://whatsapp.com/channel/..."
              className="input w-full"
            />
            <p className="mt-1 text-xs text-stone-500">Para canal público (ex.: mb.OFERTAS), use o link do canal.</p>
          </div>
          <button type="submit" disabled={submitting} className="btn-primary disabled:opacity-50">
            {submitting ? "Salvando…" : "Adicionar"}
          </button>
        </form>
      </div>

      <ul className="space-y-3">
        {channels.length === 0 && (
          <li className="card-flat p-6 text-center text-stone-500">
            Nenhum canal. Adicione um para usar &quot;Enviar para o WhatsApp&quot; nas campanhas.
          </li>
        )}
        {channels.map((c) => (
          <li key={c.id} className="card flex items-center justify-between p-4">
            <div>
              <p className="font-medium text-stone-900">{c.name}</p>
              <p className="text-sm text-stone-500">{c.channel_link ? c.channel_link : c.phone || "—"}</p>
            </div>
            <button
              type="button"
              onClick={() => handleDelete(c.id)}
              className="rounded px-3 py-1.5 text-sm text-red-600 hover:bg-red-50"
            >
              Remover
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
