# Salmo do Dia – Loja e site

Site moderno para o projeto **Salmo do Dia**: loja (e-books e afiliados Amazon), página de salmos e crescimento de audiência.

## Requisitos

- **Node.js 18.17 ou superior** (recomendado: 20 LTS).  
  O projeto não roda com Node 12 ou 14 (Next.js 14 e dependências exigem Node 18+).

**Como usar Node 18 no seu ambiente:**

- **nvm** (Node Version Manager):
  ```bash
  nvm install 18
  nvm use 18
  # ou, dentro da pasta do projeto: nvm use   (usa o .nvmrc)
  ```
- **fnm**: `fnm use` (lê o `.nvmrc`).
- **Site oficial**: [nodejs.org](https://nodejs.org/) — baixe a versão 20 LTS.

Depois:
```bash
npm install
npm run dev
```

## Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **TailwindCSS**
- **ShadCN UI** (componentes base)
- **Vercel-ready**

## Estrutura

```
/app          # Rotas e layouts (App Router)
/components   # Componentes reutilizáveis (layout, home, loja, salmos, ui)
/data         # Dados mock (produtos, salmos, afiliados)
/lib          # Utils, constantes (redes sociais, sanitização)
/public       # Assets estáticos
```

## Desenvolvimento

Com Node 18+ ativo:

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev
```

Acesse [http://localhost:3000](http://localhost:3000).

## Build e produção

```bash
npm run build
npm start
```

## Deploy na Vercel

1. Conecte o repositório à [Vercel](https://vercel.com).
2. **Root Directory**: defina como `stores/salmo_dia` se o repositório for a raiz do monorepo, ou deixe em branco se este projeto for a raiz.
3. **Build Command**: `npm run build`
4. **Output Directory**: padrão (Next.js)
5. Variáveis de ambiente (opcional): em **Settings → Environment Variables** adicione `NEXT_PUBLIC_SITE_URL` com a URL final (ex: `https://salmododia.com.br`).

### Se der 404 no Vercel

O 404 costuma acontecer quando o Vercel está fazendo build **na raiz do repositório** em vez da pasta deste projeto (Next.js só existe em `stores/salmo_dia`).

**Passos para corrigir e fazer redeploy:**

1. Abra o [Dashboard da Vercel](https://vercel.com/dashboard) e selecione o projeto do Salmo do Dia.
2. Vá em **Settings** → **General**.
3. Em **Root Directory**, clique em **Edit** e defina:
   - Se o repositório conectado for **youtube-content-automation**: use `stores/salmo_dia`.
   - Se o repositório for o **pai** (ex.: GitProjects ou data-engineering-tools): use o caminho até esta pasta, ex.: `data-engineering-tools/youtube-content-automation/stores/salmo_dia`.
4. Deixe **Framework Preset** = Next.js (detectado automaticamente).
5. **Build Command**: `npm run build` (ou em branco para usar o padrão).
6. **Install Command**: `npm install` (ou em branco).
7. **Output Directory**: em branco (padrão do Next.js).
8. Salve e vá em **Deployments** → no último deploy, clique nos **três pontinhos** → **Redeploy** (ou faça um novo commit e aguarde o deploy automático).

Depois do redeploy, a home e as rotas devem responder normalmente.

## Funcionalidades

- **Home**: hero, salmo do dia (dinâmico), destaque de produtos, CTAs.
- **Loja** (`/loja`): produtos digitais (e-books) e afiliados Amazon; cards com imagem, título, descrição, preço ou “Ver na Amazon”.
- **Produto** (`/loja/[slug]`): página do produto; checkout simulado para digitais; botão “Ver na Amazon” com log de clique para afiliados.
- **Checkout** (`/checkout?product=slug`): fluxo simulado; preparado para Stripe no futuro.
- **Salmos** (`/salmos`): lista de salmos (mock).
- **Salmo** (`/salmos/[slug]`): leitura com tipografia e sanitização básica (XSS).
- **Header/Footer**: links (Início, Salmos, Loja) e ícones para TikTok, YouTube, Instagram, Facebook, Twitter.
- **Botão flutuante**: redes sociais.
- **SEO**: metadata dinâmica, Open Graph, `sitemap.xml`, `robots.txt`.

## Dados mock

- `data/products.ts` – produtos (digitais e afiliados).
- `data/salmos.ts` – salmos para listagem e página individual.
- `data/affiliates.ts` – produtos afiliados e `logAffiliateClick()`.

Substitua por API ou CMS quando for integrar backend.

## Segurança

- Sanitização de texto na exibição de salmos (`lib/utils.ts`: `sanitizeText`).
- Estrutura pronta para autenticação (ex.: NextAuth) no futuro.
- Checkout e rotas sensíveis não indexadas (robots).

## Licença

Uso interno do projeto Salmo do Dia.
