# Baileys vs whatsapp-web.js (escolha da biblioteca)

Comparação objetiva para o uso neste projeto: **postar ofertas em canal público WhatsApp (ex.: mb.OFERTAS)** via GitHub Actions ou servidor.

## Resumo

| Critério | whatsapp-web.js | Baileys (WhiskeySockets) |
|----------|-----------------|---------------------------|
| **Canal público (link/código)** | ✅ `getChannelByInviteCode()` — suporte estável | ✅ Suporte a newsletter no main (merge 2024); JID `@newsletter` |
| **Autenticação** | QR no navegador (Puppeteer), LocalAuth | Multidevice por socket; sem browser |
| **Peso / recurso** | Pesado (Chromium headless no GHA) | Leve (só Node, sem browser) |
| **Manutenção** | Muito ativo, comunidade grande | Ativo (fork WhiskeySockets), menor |
| **Estabilidade** | Relatos de desconexão em ambas; web.js mais usado em produção | Issues de websocket fechando e desconexão com certa frequência |
| **Uso no GHA** | Funciona (cache de sessão + Puppeteer) | Teoricamente melhor (sem Chrome), mas auth/sessão diferente |

## Conclusão para este projeto

**Recomendação: manter whatsapp-web.js.**

1. **Canal por link já resolvido:** o bot aceita a URL do canal (ex.: `https://whatsapp.com/channel/0029VbBg6l4DDmFNz3FmUe2T`) ou o código no `CHAT_IDS` e usa `getChannelByInviteCode()` — fluxo estável e documentado.
2. **Stack atual estável:** QR + LocalAuth + cache no GHA já estão integrados e testados; migrar para Baileys exige outro fluxo de auth e armazenamento de credenciais.
3. **Baileys:** suporte a canal (newsletter) existe no main, mas há relatos de imagens em branco em alguns dispositivos e de desconexões/websocket; para “postar no canal de forma confiável” hoje, whatsapp-web.js ainda é a opção mais previsível.
4. **Se no futuro** o peso do Puppeteer no GHA ou limites do WhatsApp forem um problema, vale reavaliar Baileys (auth por socket, sem browser) e conferir o estado atual do suporte a newsletter e da estabilidade.

## Referências

- [whatsapp-web.js – getChannelByInviteCode](https://docs.wwebjs.dev/Client.html#getChannelByInviteCode)
- [Baileys – feat: full newsletter support (PR #822)](https://github.com/WhiskeySockets/Baileys/pull/822)
- [Baileys – send message to channel (issue #1012)](https://github.com/WhiskeySockets/Baileys/issues/1012)
