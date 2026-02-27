# Scripts – Busca automática de ofertas

## fetch-ofertas

Busca ofertas da **Amazon** e do **Mercado Livre** e grava no banco como produtos pendentes.

### Como rodar

```bash
cd backend
npm run fetch-ofertas
```

Requer `DATABASE_URL` no `.env`.

### Onde configurar as URLs

1. **Arquivo** `scripts/ofertas-urls.json` – campo `urls` (array de strings):
   - Páginas de **listagem** (ex.: Amazon Ofertas do Dia, ML Ofertas): o script extrai os links dos produtos e depois scrape cada um.
   - Páginas de **produto** (um item): o script scrape direto e insere.

2. **Arquivo** `scripts/ofertas-urls.txt` – uma URL por linha (alternativa ao JSON).

3. **Variável de ambiente** `OFERTAS_URLS` – URLs separadas por vírgula, `;` ou quebra de linha.

Exemplo `ofertas-urls.json`:

```json
{
  "urls": [
    "https://www.amazon.com.br/deals",
    "https://www.mercadolivre.com.br/ofertas",
    "https://www.amazon.com.br/dp/B0XXXXXX"
  ]
}
```

### Agendamento (cron)

Exemplo para rodar todo dia às 9h e 14h:

```cron
0 9,14 * * * cd /caminho/para/mb-ofertas/backend && npm run fetch-ofertas
```

### Comportamento

- **Listagem**: até 15 produtos por URL de listagem; intervalo de ~2,5 s entre requisições.
- **Produto único**: scrape e inserção direta.
- Produtos entram com status **pending**; aprovar no painel antes de usar em campanhas.
