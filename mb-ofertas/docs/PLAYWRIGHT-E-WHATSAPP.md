# Playwright (preços) e WhatsApp mais automático

Guia do que fazer para: (1) pegar preços corretos com browser real (Playwright) e (2) enviar mensagens para o WhatsApp de forma mais automática.

---

## 1) Playwright para preços corretos

### Por que Playwright (e não só Puppeteer)

- **Playwright**: suporta Chromium, Firefox e WebKit; API estável; bom para rodar em servidor (Render, VPS).
- **Puppeteer**: só Chromium; também funciona, mas em ambiente serverless/sem GUI você precisa de Chrome headless (mesmas exigências de binário).

Recomendação: **Playwright** com Chromium, por ser bem documentado e fácil de usar em fallback (“se fetch falhar, tenta com browser”).

### O que você precisa fazer

#### 1.1 Instalar e configurar no backend

```bash
cd backend
yarn add playwright
# ou: npm install playwright
```

Na primeira vez, instalar os browsers (só Chromium é suficiente):

```bash
npx playwright install chromium
npx playwright install-deps   # dependências do sistema (Linux: libs para Chromium)
```

#### 1.2 Onde encaixar no seu código

- Hoje: `scrape-url.service.ts` usa `fetch` + Cheerio. Quando o preço não vem no HTML (página dinâmica), dá erro “Não foi possível obter o preço”.
- Ideia: **fallback com browser**: se o scrape com `fetch` falhar (ou retornar preço 0 para ML/Shopee), chamar uma função que abre a URL no Playwright, espera a página carregar (e opcionalmente o seletor de preço), pega o HTML e reutiliza a mesma lógica de extração (Cheerio em cima do HTML renderizado).

Passos no código:

1. Criar um serviço separado, por exemplo `browser-scraper.service.ts`, que:
   - inicia o browser (ou reutiliza uma instância),
   - faz `page.goto(url)` com timeout,
   - espera um seletor de preço (ex.: ML usa classes específicas; você pode usar `page.waitForSelector(..., { timeout: 10000 })`),
   - chama `page.content()` e devolve o HTML.
2. Em `scrape-url.service.ts` (ou no ponto que chama `scrapeProductFromUrl`):
   - primeiro tenta o fluxo atual (fetch + Cheerio);
   - se der erro “Não foi possível obter o preço” (ou título), chama o browser-scraper para obter o HTML e roda a **mesma** extração (Cheerio) em cima desse HTML.

Assim você não duplica regras de preço: só troca a fonte do HTML (fetch vs browser).

#### 1.3 Variável de ambiente

- Exemplo: `USE_BROWSER_SCRAPER=true` para ativar o fallback com Playwright.
- Quando `false` ou não definida, mantém só fetch (comportamento atual).

#### 1.4 Deploy (ex.: Render)

- O Render (e a maioria dos PaaS) **não** traz Chromium instalado. Você precisa:
  - **Opção A – Docker**: usar uma imagem que já tenha Chromium/Playwright (ex.: `mcr.microsoft.com/playwright:v1.40.0-jammy` ou imagem base com Playwright).
  - **Opção B – Buildpack**: se o Render suportar, usar um buildpack que instale Chrome/Chromium e as libs (por exemplo `https://github.com/jontewks/puppeteer-buildpack` ou equivalente para Playwright).
  - **Opção C – VPS**: em um VPS (DigitalOcean, etc.) você instala as dependências uma vez (`playwright install-deps` + `playwright install chromium`) e roda o Node lá; aí o fallback com browser funciona sem mudar código.

Resumo: em ambiente “serverless” ou Render sem Docker, o fallback com browser **só funciona** se você prover o binário do Chromium (Docker ou buildpack). No seu PC ou VPS, basta instalar Playwright e os browsers.

---

## 2) WhatsApp mais automático

Hoje o fluxo é: “Abrir canal” + “mensagem copiada” → você cola no canal e envia. Isso é manual.

Para ficar **mais automático**, as opções reais são:

### 2.1 Enviar para **números** (contatos) – já suportado

- O backend já tem integração com **Twilio** (WhatsApp Business API): envia mensagem para um **número** (contato).
- Fluxo: você cadastra números em “Enviar agora” e a fila (BullMQ + Redis) manda as mensagens via Twilio.
- O que falta (se quiser): melhorar a UX para escolher “enviar para estes números” a partir de uma lista ou arquivo, em vez de colar números manualmente.

**Passos:**

1. Ter conta Twilio e número WhatsApp Business aprovado.
2. Preencher no `.env`: `WHATSAPP_ACCOUNT_SID`, `WHATSAPP_AUTH_TOKEN`, `WHATSAPP_FROM_NUMBER`.
3. Usar “Enviar agora” com a lista de números; as mensagens saem sozinhas (respeitando delay e fila).

Isso **não** posta no seu **canal** (mb.OFERTAS); posta em chats individuais. Para canal, veja abaixo.

### 2.2 Postar no **canal** (mb.OFERTAS) de forma automática

- A **API oficial do WhatsApp (Meta)** hoje permite enviar para **números** (e grupos em alguns casos), **não** para “canais” como produto separado. Ou seja: não existe endpoint “postar mensagem no canal X” na API oficial.
- Por isso, hoje a solução é mesmo: abrir o link do canal e colar (que o sistema já faz: copia + abre o link).

Para **automatizar** o “colar no canal” você teria:

- **Automação no seu computador** (só quando você está com o PC ligado):
  - Ferramenta que, no horário do agendamento, abre o link do canal no navegador e cola o texto (ex.: Puppeteer/Playwright controlando o Chrome com WhatsApp Web, ou extensão que cola no campo de mensagem). Isso é frágil (mudanças no layout do WhatsApp Web) e pode conflitar com os termos de uso.
- **Serviços de terceiros** que “postam no canal” geralmente usam alguma dessas automações por baixo; não há API oficial “postar no canal”.

Conclusão: para **canal**, o fluxo “copiar + abrir link do canal” continua sendo o suportado de forma estável. O que dá para fazer é:
- Deixar o **agendamento** bem claro (data/hora) e o botão “Abrir no WhatsApp” abrindo o canal e já com a mensagem na área de transferência.
- Opcional: no futuro, se a Meta liberar API para canais, aí sim daria para enviar direto pelo backend.

### 2.3 Resumo prático – o que fazer

| Objetivo                         | O que fazer |
|----------------------------------|-------------|
| Enviar **para números** (contatos) | Usar Twilio + fila (já existe). Configurar credenciais e “Enviar agora” com lista de números. |
| “Postar” **no canal**            | Manter “Abrir canal” + copiar mensagem. Melhorar só a UX (um clique, link certo, texto copiado). |
| Automatizar 100% o canal         | Não há API oficial. Alternativas são automação local (browser) ou aguardar suporte da Meta a canais. |

Se você disser se quer priorizar “envio para números” ou “melhorar o fluxo do canal (um clique)”, dá para detalhar os passos exatos no código (quais telas/rotas alterar).

---

## Checklist rápido

**Playwright (preços):**

- [ ] `yarn add playwright` no backend
- [ ] `npx playwright install chromium` (e `install-deps` no Linux)
- [ ] Criar `browser-scraper.service.ts` (abre URL, retorna HTML)
- [ ] Em `scrape-url.service.ts` ou no chamador: em caso de falha de preço, chamar o browser-scraper e reutilizar a extração com Cheerio
- [ ] Variável `USE_BROWSER_SCRAPER=true` para ativar
- [ ] No deploy: Docker com Playwright/Chromium ou buildpack/VPS com Chromium instalado

**WhatsApp:**

- [ ] Para envio automático a **números**: configurar Twilio no `.env` e usar “Enviar agora”
- [ ] Para **canal**: manter “Abrir canal” + copiar; melhorar UX se quiser (um clique, mensagem já copiada)

**Implementado neste projeto:** o fallback já está integrado. Ative com `USE_BROWSER_SCRAPER=true` no `.env`. Quando o scrape com `fetch` falhar por “Não foi possível obter o preço” ou “título”, o backend tenta obter o HTML com Playwright e repete a extração. Em deploy (ex.: Render) é preciso usar Docker com Chromium ou buildpack que instale o browser.
