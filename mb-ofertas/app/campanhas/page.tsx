"use client";

import { useEffect, useState } from "react";
import { api, type Campaign, type Product, type WhatsAppChannel, type WhatsAppScheduled } from "@/lib/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [channels, setChannels] = useState<WhatsAppChannel[]>([]);
  const [scheduled, setScheduled] = useState<WhatsAppScheduled[]>([]);
  const [loading, setLoading] = useState(true);
  const [sendModal, setSendModal] = useState<Campaign | null>(null);
  const [whatsappModal, setWhatsappModal] = useState<Campaign | null>(null);
  const [scheduleModal, setScheduleModal] = useState<Campaign | null>(null);
  const [phones, setPhones] = useState("");
  const [sending, setSending] = useState(false);
  const [selectedChannelId, setSelectedChannelId] = useState("");
  const [openingWhatsapp, setOpeningWhatsapp] = useState(false);
  const [scheduleDate, setScheduleDate] = useState("");
  const [scheduleTime, setScheduleTime] = useState("");
  const [scheduling, setScheduling] = useState(false);
  const [selectedForBulk, setSelectedForBulk] = useState<Set<string>>(new Set());
  const [bulkScheduleOpen, setBulkScheduleOpen] = useState(false);
  const [bulkStartDate, setBulkStartDate] = useState("");
  const [bulkStartTime, setBulkStartTime] = useState("");
  const [bulkScheduling, setBulkScheduling] = useState(false);

  function loadScheduled() {
    api<{ scheduled: WhatsAppScheduled[] }>("/whatsapp/scheduled")
      .then((d) => setScheduled(d.scheduled))
      .catch(console.error);
  }

  useEffect(() => {
    Promise.all([
      api<{ campaigns: Campaign[] }>("/campaigns?limit=50"),
      api<{ products: Product[] }>("/products?status=approved&limit=100"),
      api<{ channels: WhatsAppChannel[] }>("/whatsapp/channels"),
    ])
      .then(([c, p, ch]) => {
        setCampaigns(c.campaigns);
        setProducts(p.products);
        setChannels(ch.channels);
        if (ch.channels.length > 0 && !selectedChannelId) setSelectedChannelId(ch.channels[0].id);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
    loadScheduled();
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

  async function handleEnviarParaWhatsApp() {
    const campaign = whatsappModal;
    if (!campaign) return;
    const channel = channels.find((c) => c.id === selectedChannelId);
    if (!channel) {
      alert("Selecione um canal. Cadastre em Canais WhatsApp.");
      return;
    }
    setOpeningWhatsapp(true);
    try {
      const { message } = await api<{ message: string }>(`/campaigns/${campaign.id}/whatsapp-message`);
      if (channel.channel_link) {
        await navigator.clipboard.writeText(message);
        window.open(channel.channel_link, "_blank", "noopener,noreferrer");
        alert("Canal aberto. A mensagem foi copiada — cole no canal e envie.");
      } else {
        const phone = channel.phone.startsWith("55") ? channel.phone : "55" + channel.phone;
        window.open(`https://wa.me/${phone}?text=${encodeURIComponent(message)}`, "_blank", "noopener,noreferrer");
      }
      setWhatsappModal(null);
    } catch (e) {
      console.error(e);
      alert("Erro ao gerar mensagem.");
    } finally {
      setOpeningWhatsapp(false);
    }
  }

  async function handleProgramar() {
    const campaign = scheduleModal;
    if (!campaign) return;
    const channel = channels.find((c) => c.id === selectedChannelId);
    if (!channel) {
      alert("Selecione um canal.");
      return;
    }
    const at = `${scheduleDate}T${scheduleTime}:00`;
    if (!scheduleDate || !scheduleTime) {
      alert("Informe data e hora.");
      return;
    }
    setScheduling(true);
    try {
      const { message } = await api<{ message: string }>(`/campaigns/${campaign.id}/whatsapp-message`);
      await api("/whatsapp/scheduled", {
        method: "POST",
        body: JSON.stringify({ channelId: channel.id, message, scheduledAt: at }),
      });
      loadScheduled();
      setScheduleModal(null);
      setScheduleDate("");
      setScheduleTime("");
      alert("Agendamento salvo. Abra em Agendamentos quando for a hora.");
    } catch (e) {
      console.error(e);
      alert("Erro ao programar.");
    } finally {
      setScheduling(false);
    }
  }

  function toggleBulkSelect(id: string) {
    setSelectedForBulk((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function handleBulkSchedule() {
    const channel = channels.find((c) => c.id === selectedChannelId);
    if (!channel) {
      alert("Selecione um canal.");
      return;
    }
    const ids = Array.from(selectedForBulk);
    if (ids.length === 0) {
      alert("Selecione ao menos uma campanha.");
      return;
    }
    if (!bulkStartDate || !bulkStartTime) {
      alert("Informe data e hora de início.");
      return;
    }
    const startAt = `${bulkStartDate}T${bulkStartTime}:00`;
    setBulkScheduling(true);
    try {
      const data = await api<{ created: number; ids: string[] }>("/whatsapp/scheduled/bulk", {
        method: "POST",
        body: JSON.stringify({
          channelId: channel.id,
          campaignIds: ids,
          startAt,
          intervalMinutes: 10,
        }),
      });
      loadScheduled();
      setSelectedForBulk(new Set());
      setBulkScheduleOpen(false);
      setBulkStartDate("");
      setBulkStartTime("");
      alert(`${data.created} agendamento(s) criado(s). Abra em Agendamentos no horário de cada um.`);
    } catch (e) {
      console.error(e);
      alert("Erro ao programar em massa.");
    } finally {
      setBulkScheduling(false);
    }
  }

  async function handleAbrirAgendado(item: WhatsAppScheduled) {
    try {
      const data = await api<{ message: string; channelPhone: string; channelLink: string | null; url: string | null }>(
        `/whatsapp/scheduled/${item.id}/open`,
        { method: "POST" }
      );
      if (data.channelLink) {
        await navigator.clipboard.writeText(data.message);
        window.open(data.channelLink, "_blank", "noopener,noreferrer");
        alert("Canal aberto. A mensagem foi copiada — cole no canal e envie.");
      } else {
        const url = `https://wa.me/${data.channelPhone}?text=${encodeURIComponent(data.message)}`;
        window.open(url, "_blank", "noopener,noreferrer");
      }
      loadScheduled();
    } catch (e) {
      console.error(e);
      alert("Erro ao abrir.");
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <p className="text-stone-500">Carregando campanhas…</p>
      </div>
    );
  }

  const now = new Date();
  const today = now.toISOString().slice(0, 10);
  const defaultTime = now.getHours().toString().padStart(2, "0") + ":" + (now.getMinutes() + 1).toString().padStart(2, "0");

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Campanhas</h1>
          <p className="page-subtitle">Envie ofertas por WhatsApp para sua lista.</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {selectedForBulk.size > 0 && (
            <button
              type="button"
              onClick={() => {
                setBulkScheduleOpen(true);
                setBulkStartDate(today);
                setBulkStartTime(defaultTime);
              }}
              className="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-medium text-stone-700 hover:bg-stone-50"
            >
              Programar em massa ({selectedForBulk.size})
            </button>
          )}
          <a href="/campanhas/nova" className="btn-primary">
            Nova campanha
          </a>
        </div>
      </div>

      <ul className="space-y-4">
        {campaigns.length === 0 && (
          <li className="card-flat p-8 text-center text-stone-500">
            Nenhuma campanha. Crie uma e adicione produtos aprovados.
          </li>
        )}
        {campaigns.map((c) => (
          <li key={c.id} className="card flex items-center justify-between p-5">
            <div className="flex min-w-0 flex-1 items-center gap-3">
              <label className="flex shrink-0 items-center gap-2">
                <input
                  type="checkbox"
                  checked={selectedForBulk.has(c.id)}
                  onChange={() => toggleBulkSelect(c.id)}
                  className="h-4 w-4 rounded border-stone-300"
                />
                <span className="sr-only">Selecionar para programar em massa</span>
              </label>
              <div className="min-w-0">
                <p className="font-semibold text-stone-900">{c.name}</p>
                <p className="text-sm text-stone-500">
                  Status: {c.status} • {c.product_ids?.length ?? 0} produto(s)
                </p>
              </div>
            </div>
            <div className="flex shrink-0 flex-wrap gap-2">
              {["draft", "scheduled"].includes(c.status) && (
                <button onClick={() => setSendModal(c)} className="btn-primary text-sm">
                  Enviar agora
                </button>
              )}
              <button
                onClick={() => setWhatsappModal(c)}
                className="rounded-lg border border-amber-600 bg-amber-50 px-4 py-2 text-sm font-medium text-amber-800 hover:bg-amber-100"
              >
                Enviar para WhatsApp
              </button>
              <button
                onClick={() => {
                  setScheduleModal(c);
                  setScheduleDate(today);
                  setScheduleTime(defaultTime);
                }}
                className="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-medium text-stone-700 hover:bg-stone-50"
              >
                Programar
              </button>
              <a href={`/campanhas/${c.id}`} className="btn-secondary text-sm">
                Ver
              </a>
            </div>
          </li>
        ))}
      </ul>

      {scheduled.length > 0 && (
        <section className="mt-8">
          <h2 className="mb-3 text-lg font-semibold text-stone-800">Agendamentos WhatsApp</h2>
          <ul className="space-y-2">
            {scheduled.map((s) => (
              <li key={s.id} className="card flex items-center justify-between p-4">
                <div className="min-w-0">
                  <p className="font-medium text-stone-900">{s.channel_name ?? s.channel_id}</p>
                  <p className="text-sm text-stone-500">
                    {new Date(s.scheduled_at).toLocaleString("pt-BR")} • {s.status === "opened" ? "Aberto" : "Pendente"}
                  </p>
                </div>
                {s.status === "pending" && (
                  <button
                    onClick={() => handleAbrirAgendado(s)}
                    className="shrink-0 rounded-lg bg-green-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-green-700"
                  >
                    Abrir no WhatsApp
                  </button>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

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

      {whatsappModal && (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50">
          <div className="card-flat w-full max-w-md p-6 shadow-xl">
            <h3 className="mb-2 font-semibold text-stone-900">Enviar para WhatsApp: {whatsappModal.name}</h3>
            <p className="mb-4 text-sm text-stone-600">
              Selecione o canal. O WhatsApp abrirá com a mensagem pronta; é só enviar.
            </p>
            <div className="mb-4">
              <label className="mb-1 block text-sm font-medium text-stone-700">Canal</label>
              <select
                value={selectedChannelId}
                onChange={(e) => setSelectedChannelId(e.target.value)}
                className="input w-full"
              >
                {channels.length === 0 && <option value="">Cadastre canais em Canais WhatsApp</option>}
                {channels.map((ch) => (
                  <option key={ch.id} value={ch.id}>
                    {ch.name} {ch.channel_link ? "(canal)" : `(${ch.phone})`}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex justify-end gap-2">
              <button onClick={() => setWhatsappModal(null)} className="btn-secondary">
                Cancelar
              </button>
              <button
                onClick={handleEnviarParaWhatsApp}
                disabled={openingWhatsapp || channels.length === 0}
                className="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
              >
                {openingWhatsapp ? "Abrindo…" : "Abrir WhatsApp"}
              </button>
            </div>
          </div>
        </div>
      )}

      {scheduleModal && (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50">
          <div className="card-flat w-full max-w-md p-6 shadow-xl">
            <h3 className="mb-2 font-semibold text-stone-900">Programar: {scheduleModal.name}</h3>
            <p className="mb-4 text-sm text-stone-600">
              Escolha o canal e quando postar. No horário, abra &quot;Agendamentos&quot; e clique em &quot;Abrir no WhatsApp&quot;.
            </p>
            <div className="mb-4">
              <label className="mb-1 block text-sm font-medium text-stone-700">Canal</label>
              <select
                value={selectedChannelId}
                onChange={(e) => setSelectedChannelId(e.target.value)}
                className="input w-full"
              >
                {channels.map((ch) => (
                  <option key={ch.id} value={ch.id}>
                    {ch.name} {ch.channel_link ? "(canal)" : `(${ch.phone})`}
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-4 grid grid-cols-2 gap-3">
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-700">Data</label>
                <input
                  type="date"
                  value={scheduleDate}
                  onChange={(e) => setScheduleDate(e.target.value)}
                  className="input w-full"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-700">Horário</label>
                <input
                  type="time"
                  value={scheduleTime}
                  onChange={(e) => setScheduleTime(e.target.value)}
                  className="input w-full"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <button onClick={() => setScheduleModal(null)} className="btn-secondary">
                Cancelar
              </button>
              <button
                onClick={handleProgramar}
                disabled={scheduling}
                className="btn-primary disabled:opacity-50"
              >
                {scheduling ? "Salvando…" : "Programar"}
              </button>
            </div>
          </div>
        </div>
      )}

      {bulkScheduleOpen && (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/50">
          <div className="card-flat w-full max-w-md p-6 shadow-xl">
            <h3 className="mb-2 font-semibold text-stone-900">Programar em massa</h3>
            <p className="mb-4 text-sm text-stone-600">
              {selectedForBulk.size} campanha(s) selecionada(s). Será criado um agendamento a cada 10 minutos, na ordem da lista.
            </p>
            <div className="mb-4">
              <label className="mb-1 block text-sm font-medium text-stone-700">Canal</label>
              <select
                value={selectedChannelId}
                onChange={(e) => setSelectedChannelId(e.target.value)}
                className="input w-full"
              >
                {channels.map((ch) => (
                  <option key={ch.id} value={ch.id}>
                    {ch.name} {ch.channel_link ? "(canal)" : `(${ch.phone})`}
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-4 grid grid-cols-2 gap-3">
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-700">Data início</label>
                <input
                  type="date"
                  value={bulkStartDate}
                  onChange={(e) => setBulkStartDate(e.target.value)}
                  className="input w-full"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-stone-700">Horário início</label>
                <input
                  type="time"
                  value={bulkStartTime}
                  onChange={(e) => setBulkStartTime(e.target.value)}
                  className="input w-full"
                />
              </div>
            </div>
            <p className="mb-4 text-xs text-stone-500">Intervalo: 10 minutos entre cada post.</p>
            <div className="flex justify-end gap-2">
              <button onClick={() => setBulkScheduleOpen(false)} className="btn-secondary">
                Cancelar
              </button>
              <button
                onClick={handleBulkSchedule}
                disabled={bulkScheduling}
                className="btn-primary disabled:opacity-50"
              >
                {bulkScheduling ? "Criando…" : "Criar agendamentos"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
