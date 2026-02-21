# Como preencher o .env com Supabase

O backend usa **conexão direta ao PostgreSQL**. As chaves “publishable”, “anon”, “service_role” são da **API do Supabase** (Auth/REST); para o MB-Ofertas precisamos principalmente da **URL de conexão do banco**.

## 1. DATABASE_URL (obrigatório)

É a **connection string do PostgreSQL**, não a URL da API.

1. No Supabase: **Project Settings** (ícone engrenagem) → **Database**.
2. Em **Connection string** escolha:
   - **URI** (Connection pooling) – recomendado: usa porta **6543** (pooler).
   - Ou **Direct connection** – porta **5432**.
3. Copie a URI. Ela parece com:
   ```text
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
4. Substitua **`[YOUR-PASSWORD]`** pela senha do banco (a que você definiu ao criar o projeto).
5. Se houver caracteres especiais na senha, use URL encode (ex.: `@` → `%40`).

No `.env`:

```env
DATABASE_URL=postgresql://postgres.abc123:MinHaS3nha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

## 2. Chaves da API Supabase (opcional por enquanto)

Em **Project Settings** → **API** você vê:

| Variável no .env           | No painel Supabase | Uso no MB-Ofertas      |
|---------------------------|--------------------|-------------------------|
| `SUPABASE_URL`            | Project URL        | Base da API (futuro)    |
| `SUPABASE_ANON_KEY`       | anon / public      | Cliente público (futuro)|
| `SUPABASE_SERVICE_ROLE_KEY` | service_role     | Backend com acesso total (futuro) |

- **anon key** (ou “publishable” / “anon public”): pode ir no frontend; acesso respeitando RLS.
- **service_role**: só no backend, nunca no frontend; ignora RLS.

O projeto atual usa apenas **PostgreSQL via `pg`** com `DATABASE_URL`. As variáveis `SUPABASE_*` podem ficar no `.env` para quando você for usar Auth ou a REST API do Supabase.

## Resumo

- Para rodar migrations e a API: preencha **só o `DATABASE_URL`** com a connection string do **Database** (passo 1).
- As outras (URL, anon key, service_role, etc.) são da API; pode colocá-las em `SUPABASE_URL`, `SUPABASE_ANON_KEY` e `SUPABASE_SERVICE_ROLE_KEY` se quiser usar depois.
