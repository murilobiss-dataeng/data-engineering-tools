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
| `CHAT_ID` | ID do canal (ex.: `120363405814099508@newsletter`). Única variável de destino. |
| `CRON_INTERVAL_MINUTES` | Intervalo em minutos entre cada verificação (padrão: 10) |
| `DELAY_BETWEEN_POSTS_MINUTES` | Pausa em minutos entre cada post enviado (padrão: 10). Evita flood no canal. |
| `DATA_PATH` | Pasta para sessão e arquivo de enviados (padrão: `./data`) |
| `AUTH_CLIENT_ID` | Id da sessão LocalAuth (padrão: `channel_bot`) |
| `SKIP_POSTS_WITHOUT_IMAGE` | Se `true` (padrão), não envia posts sem imagem. Use `false` para enviar também só texto. |

### WhatsApp Business vs WhatsApp normal (Messenger)

O bot usa o **mesmo** fluxo que [web.whatsapp.com](https://web.whatsapp.com): o QR é **um só**; quem define se a sessão é **pessoal** ou **Business** é o **app no telefone** que você usa para escanear.

- Para vincular a conta **Business**: abra o app **WhatsApp Business** → menu (⋮ ou ⚙) → **Aparelhos conectados** → **Conectar um aparelho** e escaneie o QR (não use o app WhatsApp “verde” para isso).
- Para vincular a conta **pessoal**: use o **WhatsApp** normal no mesmo caminho (**Aparelhos conectados**).

Se **só** o Messenger completar o pareamento e o **Business** falhar ou não oferecer “Conectar”:

1. No telefone, em **ambos** os apps (se tiver os dois), veja **Aparelhos conectados** e **desconecte** sessões antigas do WhatsApp Web.
2. Apague a sessão local do bot: remova a pasta `data/.wwebjs_auth` (ou mude `AUTH_CLIENT_ID` no `.env` para gerar uma sessão nova, ex.: `channel_bot_wa_business`).
3. Atualize o **WhatsApp Business** na loja e tente de novo; em contas muito antigas, confira se **multi‑dispositivo** / aparelhos ligados está ativo nas definições do WhatsApp.

**Patch:** é aplicado um patch em `whatsapp-web.js` (via `patch-package`) para evitar erro ao enviar para canal público quando `channelMetadata.description` não vem na resposta (`Cannot read properties of undefined (reading 'description')`). O `postinstall` aplica o patch após `npm install`.

### Formato da API / Feed mb-ofertas

O endpoint **GET /api/products/feed** da API mb-ofertas (backend no Render) retorna os produtos aprovados no formato esperado pelo bot:

```json
[
  {
    "title": "Nome do produto",
    "text": "Nome do produto\n\n... preço, link ...",
    "url": "https://...",
    "imageUrl": "https://..."
  }
]
```

- **Imagem é prioridade:** o feed da API mb-ofertas retorna **apenas produtos que têm imagem** (`image_url`). O bot aceita `imageUrl`, `image_url` ou `image` e, por padrão, não envia posts sem imagem (`SKIP_POSTS_WITHOUT_IMAGE=true`). Se o envio por URL falhar (ex.: em GitHub Actions), o bot tenta baixar a imagem com axios e reenvia — assim o canal sempre envia ofertas com imagem para engajar.
- No mb-ofertas, aprovando produtos na interface (site na Vercel), eles entram nesse feed e o bot envia para o canal.

### Como obter o CHAT_ID

1. Inicie o bot: `npm start`
2. Escaneie o QR Code com o WhatsApp (Aparelhos conectados)
3. Depois de conectado, o bot lista "Chats disponíveis" e **Canais** com o **ID interno** (ex.: `12345678901234567@newsletter`). **Use esse ID em CHAT_ID** (prioridade). A conta precisa ser **admin do canal** para enviar.
4. Coloque no `.env`: `CHAT_ID=12345678901234567@newsletter` (canal) ou `CHAT_ID=120363XXXXXXXX@g.us` (grupo).

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
4. Envia para o canal/grupo definido em `CHAT_ID`.
5. Se o post tiver imagem (`imageUrl` / `image_url` / `image`), envia a imagem com a mensagem como legenda (com fallback por download direto se necessário). Por padrão, posts sem imagem são ignorados.
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

- **`API_URL`** — URL do feed (ex.: `https://mb-ofertas-api.onrender.com/api/products/feed`). Em free tier (ex.: Render) a API pode demorar ~1 min no primeiro request (cold start); o bot usa timeout 60s e 2 retries no GHA.
- **`CHAT_ID`** — ID do canal (ex.: `120363405814099508@newsletter`) ou do grupo (`XXX@g.us`). A conta que escaneou o QR deve ser **admin do canal**.

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
