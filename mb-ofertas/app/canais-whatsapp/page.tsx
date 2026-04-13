"use client";

import { useEffect, useState } from "react";
import { api, type WhatsAppChannel } from "@/lib/api";

export default function CanaisWhatsAppPage() {
  const [channels, setChannels] = useState<WhatsAppChannel[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [channelLink, setChannelLink] = useState("");
  const [categorySlug, setCategorySlug] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [editing, setEditing] = useState<WhatsAppChannel | null>(null);
  const [editName, setEditName] = useState("");
  const [editPhone, setEditPhone] = useState("");
  const [editChannelLink, setEditChannelLink] = useState("");
  const [editCategorySlug, setEditCategorySlug] = useState("");
  const [editSubmitting, setEditSubmitting] = useState(false);

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
      const slug = categorySlug.trim() || null;
      const created = await api<WhatsAppChannel>("/whatsapp/channels", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          phone: num ?? "",
          channelLink: link,
          categorySlug: slug,
        }),
      });
      setChannels((prev) => [...prev, created]);
      setName("");
      setPhone("");
      setChannelLink("");
      setCategorySlug("");
    } catch (err) {
      console.error(err);
      alert("Erro ao adicionar canal.");
    } finally {
      setSubmitting(false);
    }
  }

  function openEdit(c: WhatsAppChannel) {
    setEditing(c);
    setEditName(c.name);
    setEditPhone(c.phone || "");
    setEditChannelLink(c.channel_link || "");
    setEditCategorySlug(c.category_slug || "");
  }

  async function handleEditSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!editing) return;
    const link = editChannelLink.trim() || null;
    const num = editPhone.trim() || null;
    if (!link && (!num || num.replace(/\D/g, "").length < 10)) {
      alert("Preencha o número (DDD + número) ou o link do canal.");
      return;
    }
    setEditSubmitting(true);
    try {
      const updated = await api<WhatsAppChannel>(`/whatsapp/channels/${editing.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          name: editName.trim(),
          phone: num ?? "",
          channelLink: link,
          categorySlug: editCategorySlug.trim() || null,
        }),
      });
      setChannels((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
      setEditing(null);
    } catch (err) {
      console.error(err);
      alert("Erro ao atualizar canal.");
    } finally {
      setEditSubmitting(false);
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
            Cadastre os canais (números ou grupos) para o botão &quot;Enviar para o WhatsApp&quot; nas campanhas. O campo
            &quot;Tag do canal&quot; deve coincidir com a categoria das ofertas (health, tech, ofertas, faith, fitness) e com o{" "}
            <code className="rounded bg-stone-100 px-1">CHANNEL_SLUG</code> no GitHub Actions.
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
          <div className="min-w-[160px]">
            <label className="mb-1 block text-sm font-medium text-stone-600">Tag do canal (opcional)</label>
            <select
              value={categorySlug}
              onChange={(e) => setCategorySlug(e.target.value)}
              className="input w-full"
            >
              <option value="">—</option>
              <option value="health">health</option>
              <option value="tech">tech</option>
              <option value="ofertas">ofertas</option>
              <option value="faith">faith</option>
              <option value="fitness">fitness</option>
            </select>
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
              {c.category_slug && (
                <p className="text-xs text-stone-400">Canal de ofertas: {c.category_slug}</p>
              )}
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => openEdit(c)}
                className="rounded px-3 py-1.5 text-sm text-stone-600 hover:bg-stone-100"
              >
                Editar
              </button>
              <button
                type="button"
                onClick={() => handleDelete(c.id)}
                className="rounded px-3 py-1.5 text-sm text-red-600 hover:bg-red-50"
              >
                Remover
              </button>
            </div>
          </li>
        ))}
      </ul>

      {editing && (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50">
          <div className="card-flat w-full max-w-md p-6 shadow-xl">
            <h2 className="mb-4 font-semibold text-stone-900">Editar canal: {editing.name}</h2>
            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-600">Nome</label>
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="input w-full"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-600">Número (opcional)</label>
                <input
                  type="tel"
                  value={editPhone}
                  onChange={(e) => setEditPhone(e.target.value)}
                  placeholder="11999999999"
                  className="input w-full"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-600">Link do canal (para publicar no canal)</label>
                <input
                  type="url"
                  value={editChannelLink}
                  onChange={(e) => setEditChannelLink(e.target.value)}
                  placeholder="https://whatsapp.com/channel/..."
                  className="input w-full"
                />
                <p className="mt-1 text-xs text-stone-500">Preencha para que &quot;Enviar para WhatsApp&quot; abra o canal em vez do número.</p>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-600">Tag do canal (categoria)</label>
                <select
                  value={editCategorySlug}
                  onChange={(e) => setEditCategorySlug(e.target.value)}
                  className="input w-full"
                >
                  <option value="">—</option>
                  <option value="health">health</option>
                  <option value="tech">tech</option>
                  <option value="ofertas">ofertas</option>
                  <option value="faith">faith</option>
                  <option value="fitness">fitness</option>
                </select>
                <p className="mt-1 text-xs text-stone-500">Alinha com a categoria do produto e com o bot automatizado.</p>
              </div>
              <div className="flex justify-end gap-2">
                <button type="button" onClick={() => setEditing(null)} className="btn-secondary">
                  Cancelar
                </button>
                <button type="submit" disabled={editSubmitting} className="btn-primary disabled:opacity-50">
                  {editSubmitting ? "Salvando…" : "Salvar"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
