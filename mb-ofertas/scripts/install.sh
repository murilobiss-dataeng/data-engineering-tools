#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
echo "Instalando dependências (workspaces)..."
npm install
echo "Concluído. Próximos passos:"
echo "  1. cp .env.example .env e preencha DATABASE_URL (Supabase), REDIS_URL, WHATSAPP_*"
echo "  2. npm run db:migrate"
echo "  3. npm run dev:api   (em um terminal)"
echo "  4. npm run dev:dashboard (em outro)"
echo "  5. npm run worker   (para envio WhatsApp)"
