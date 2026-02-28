# MB Ofertas

Sistema de envio automatizado de ofertas via WhatsApp para afiliados (Amazon inicialmente), com painel web e filas com Redis.

## Estrutura

```
mb-ofertas/
├── backend/          # API Node.js + TypeScript, workers, pipeline
│   ├── src/
│   │   ├── api/      # Express, rotas, rate limit
│   │   ├── config/   # env, logger
│   │   ├── db/       # PostgreSQL (Supabase), migrations
│   │   ├── pipeline/ # Captura diária (cron)
│   │   ├── repositories/
│   │   ├── services/ # Amazon, mensagens, WhatsApp
│   │   └── workers/  # BullMQ, envio com delay
├── dashboard/        # Next.js (Vercel)
└── .env.example
```

## Requisitos

- Node.js 18+
- PostgreSQL (Supabase)
- Redis

## Instalação

1. **Clone e instale dependências**

```bash
cd mb-ofertas
npm install
```

2. **Configure o ambiente**

```bash
cp .env.example .env
# Edite .env com:
# - DATABASE_URL (Supabase: em Render ou rede sem IPv6, use "Session" no Connect → Session)
# - REDIS_URL (ex: redis://localhost:6379)
# - WHATSAPP_* (Twilio ou seu provedor)
# - AMAZON_PARTNER_TAG (se usar API/scraping)
```

3. **Banco de dados**

```bash
npm run db:migrate
```

Se o banco já existia antes da coluna `installments` (erro "column installments does not exist" em produção), rode no backend:

```bash
cd backend && npm run db:ensure-columns
```

(No Render: use **Shell** do serviço ou adicione um passo no deploy que execute `npm run db:ensure-columns` com `DATABASE_URL` configurada.)

4. **Subir API e Redis (local)**

Com Docker:

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

API:

```bash
npm run dev:api
# http://localhost:4000
```

5. **Dashboard**

```bash
npm run dev:dashboard
# http://localhost:3000
```

6. **Worker (envio WhatsApp)**

Em outro terminal:

```bash
npm run worker
```

## Uso

### Pipeline diário (captura)

- Rode manualmente: `npm run pipeline` (no backend).
- Agende com cron para 9h, 12h, 18h:
  - `0 9,12,18 * * * cd /caminho/mb-ofertas && npm run pipeline`

### Dashboard

- **Produtos**: listar, aprovar/reprovar ofertas, ver preview da mensagem.
- **Campanhas**: criar campanha (selecionar produtos aprovados), **Enviar agora** (informar lista de números).

### API

- `GET /api/products` – lista produtos (query: status, categoryId, limit, offset).
- `PATCH /api/products/:id/status` – aprovar/reprovar (body: `{ "status": "approved" | "rejected" }`).
- `POST /api/products/capture` – dispara captura Amazon (body opcional: `categorySlug`, `categoryId`).
- `POST /api/products` – cadastro manual (title, price, affiliateLink, etc.).
- `GET /api/products/:id/preview-message` – preview da copy WhatsApp.
- `GET /api/campaigns`, `POST /api/campaigns`, `GET /api/campaigns/:id`.
- `POST /api/campaigns/:id/send-now` – enfileira envio (body: `{ "recipientPhones": ["5511999999999"] }`).
- `GET /api/categories` – lista categorias.

### Limites e segurança

- Rate limit na API (configurável por `RATE_LIMIT_WINDOW_MS` e max por janela).
- Delay entre mensagens: `DELAY_BETWEEN_MESSAGES_MS` (ex: 6000 ms).
- Worker com concurrency 1 para respeitar anti-ban.

## Deploy (Vercel)

- **Dashboard**: conecte o repositório ao Vercel, root ou `dashboard/`. Configure `NEXT_PUBLIC_API_URL` para a URL da sua API em produção.
- **Backend**: hospede em Railway, Render, Fly.io ou VPS. Exponha a API e rode o worker (e opcionalmente o pipeline via cron do provedor).

## Escalabilidade

- **Amazon**: implemente `captureAmazonDeals` com Product Advertising API (paapi5) ou scraping ético (Playwright) e preencha `mapAmazonItemToProduct` com os campos reais.
- **WhatsApp**: o serviço está preparado para Twilio; para 360dialog ou outro, altere `sendWhatsAppText` em `backend/src/services/whatsapp/whatsapp.service.ts`.
- **Encurtador e cliques**: adicione um service de short link (Bitly ou interno) e salve cliques em uma tabela `link_clicks`; use o link curto em `generateOfferMessage` quando disponível.

## Licença

Uso interno / comercial conforme seu projeto.
