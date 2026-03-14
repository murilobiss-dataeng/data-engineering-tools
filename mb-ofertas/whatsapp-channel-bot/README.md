# WhatsApp Channel Bot

Bot em Node.js que consulta uma API e envia os posts automaticamente para um ou mais canais/grupos do WhatsApp, usando **whatsapp-web.js** com sessão persistente (LocalAuth).

**Integração com o projeto mb-ofertas:** o site (frontend) fica na **Vercel**; a **API** e este **bot** precisam rodar em um host **sempre ligado** (ex.: **Render**), pois o bot usa Puppeteer/Chromium e sessão em disco — não funciona em serverless (Vercel). Configure a API do mb-ofertas no Render e o bot em outro serviço (ou no mesmo) com `API_URL=https://sua-api.onrender.com/api/products/feed` para postar os **produtos aprovados** no canal.

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

## Onde rodar o bot (não pode ser na Vercel)

| Onde        | Serve para                          |
|------------|--------------------------------------|
| **Vercel** | Só o frontend (site) do mb-ofertas   |
| **Render** | API mb-ofertas + **este bot** (Background Worker ou Web Service sempre ligado) |

O bot precisa de processo contínuo e armazenamento local (sessão WhatsApp). Crie no Render um **Background Worker** (ou um segundo Web Service) com este repositório, configure `API_URL` para a URL da sua API (ex.: `https://mb-ofertas-api.onrender.com/api/products/feed`) e `CHAT_IDS`. Na primeira vez você precisará escanear o QR (logs do worker no Render); depois a sessão fica salva.

## Aviso

Este bot usa **whatsapp-web.js**, que não é oficial. O uso pode violar os termos do WhatsApp. Use por sua conta e risco; para uso crítico prefira a [API oficial do WhatsApp](https://developers.facebook.com/docs/whatsapp).
