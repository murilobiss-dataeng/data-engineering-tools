# WhatsApp Channel Bot

Bot em Node.js que consulta uma API e envia os posts automaticamente para um ou mais canais/grupos do WhatsApp, usando **whatsapp-web.js** com sessão persistente (LocalAuth).

**Integração com o projeto mb-ofertas:** o site (frontend) fica na **Vercel**; a **API** no Render (ou outro host). O bot pode rodar via **GitHub Actions** (agendado a cada 10 min) ou em um host sempre ligado (Render). Veja a seção **GitHub Actions** abaixo.

## Requisitos

- Node.js 18+
- Conta WhatsApp (será usado o WhatsApp Web; escaneie o QR code na primeira vez)

## Instalação

```bash
cd whatsapp-channel-bot
npm install
```

## Configuração

Copie o exemplo e edite:

```bash
cp .env.example .env
```

Variáveis no `.env`:

| Variável | Descrição |
|----------|-----------|
| `API_URL` | URL do **feed** da API. No mb-ofertas use: `https://SUA-API.onrender.com/api/products/feed` (produtos aprovados) |
| `CHAT_IDS` | IDs dos chats (grupos/canais) separados por vírgula. Veja abaixo como obter. |
| `CRON_INTERVAL_MINUTES` | Intervalo em minutos entre cada verificação (padrão: 10) |
| `DATA_PATH` | Pasta para sessão e arquivo de enviados (padrão: `./data`) |
| `AUTH_CLIENT_ID` | Id da sessão LocalAuth (padrão: `channel_bot`) |

### Formato da API / Feed mb-ofertas

O endpoint **GET /api/products/feed** da API mb-ofertas (backend no Render) retorna os produtos aprovados no formato esperado pelo bot:

```json
[
  {
    "title": "Nome do produto",
    "text": "* OFERTA DO DIA *\n\n... preço, link ...",
    "url": "https://...",
    "imageUrl": "https://..."
  }
]
```

- `imageUrl` é opcional; se existir, a imagem é enviada junto com a mensagem.
- No mb-ofertas, aprovando produtos na interface (site na Vercel), eles entram nesse feed e o bot envia para o canal.

### Como obter o CHAT_ID

1. Inicie o bot: `npm start`
2. Escaneie o QR Code com o WhatsApp (Aparelhos conectados)
3. Depois de conectado, o bot envia a primeira leva de posts. Nos logs ou no código você pode listar os chats: no WhatsApp Web, grupos e canais têm IDs no formato `XXXXXXXXXX@g.us` (grupos) ou do contato. Uma forma é usar um script que lista os chats após `ready` e logar os IDs.
4. Coloque o(s) ID(s) no `.env`: `CHAT_IDS=120363XXXXXXXX@c.us,YYYYYY@g.us`

## Uso

```bash
npm start
```

Na primeira execução será exibido um **QR Code** no terminal. Abra o WhatsApp no celular → Aparelhos conectados → Conectar um aparelho e escaneie. A sessão fica salva em `DATA_PATH`; nas próximas vezes o bot pode conectar sem novo QR.

**Onde fica o QR em arquivo (local):** o bot salva também em `DATA_PATH/qr-url.txt` (por padrão `whatsapp-channel-bot/data/qr-url.txt`). O caminho completo aparece no log. Você pode abrir esse arquivo no navegador (copie o conteúdo e cole na barra de endereço) para ver o QR em tela cheia.

## Comportamento

1. A cada **N minutos** (configurável), o bot chama a `API_URL`.
2. Para cada post retornado, verifica se já foi enviado (controle por `url` em `data/sent_posts.json`).
3. Monta a mensagem no formato:
   ```
   🙏 *{title}*

   {text}

   Leia completo:
   {url}
   ```
4. Envia para todos os `CHAT_IDS` (suporte a múltiplos canais).
5. Se o post tiver `imageUrl`, envia a imagem com a mensagem como legenda.
6. Se o WhatsApp desconectar, o bot tenta **reconectar** automaticamente após 30 segundos.

## Logs

- Saída no console e em `logs/bot.log`.

## Estrutura do código

- `src/config.js` – Configuração a partir do `.env`
- `src/logger.js` – Log em arquivo e console
- `src/storage.js` – Controle de posts já enviados (JSON local)
- `src/api.js` – Busca posts na API (axios)
- `src/formatter.js` – Formata a mensagem
- `src/sender.js` – Envio para WhatsApp (texto e imagem, múltiplos chats)
- `src/index.js` – Cliente WhatsApp (LocalAuth), cron e reconexão

## GitHub Actions (recomendado)

O bot pode rodar no **GitHub Actions** com execução a cada 10 minutos. A sessão do WhatsApp fica no **cache** do GHA.

### Secrets no repositório

Em **Settings → Secrets and variables → Actions** adicione:

- **`API_URL`** — URL do feed (ex.: `https://mb-ofertas-api.onrender.com/api/products/feed`)
- **`CHAT_IDS`** — ID(s) do(s) canal(is)/grupo(s), separados por vírgula

### Primeira vez: criar sessão (escanear QR)

1. No GitHub: **Actions** → **Init WhatsApp (escanear QR)** → **Run workflow**.
2. Abra a **execução** (clique no run).
3. Clique no job **“Gerar QR, link e aguardar escaneamento”**. O **QR aparece direto no resumo do job** (imagem na própria página do GHA). Não é preciso baixar artifact.
4. Escaneie com o WhatsApp no celular: **Aparelhos conectados** → **Conectar um aparelho**.
5. Aguarde o job concluir (até ~10 min). A sessão fica no cache e o workflow agendado passa a funcionar sem novo QR.

**Se a imagem do QR não carregar no resumo:** baixe o artifact **whatsapp-qr** (um único arquivo **qr.html**) no final da página e abra no navegador.

### Workflow agendado

O workflow **WhatsApp Bot (postar ofertas)** roda **a cada 10 minutos** e envia os novos produtos do feed para o(s) canal(is). Não é preciso fazer nada além de manter os secrets configurados.

### Rodar localmente (alternativa)

Se preferir rodar o bot na sua máquina ou em um servidor (ex.: Render), use `npm start` e escaneie o QR no terminal. A sessão fica em `data/`.

## Aviso

Este bot usa **whatsapp-web.js**, que não é oficial. O uso pode violar os termos do WhatsApp. Use por sua conta e risco; para uso crítico prefira a [API oficial do WhatsApp](https://developers.facebook.com/docs/whatsapp).
