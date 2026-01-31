# Expansão para TikTok e Instagram

> **Status**: Planejado. Por ora, validar o modelo apenas no YouTube.

## Visão Geral

Quando quiser publicar nos 3 canais (YouTube, TikTok, Instagram), será preciso:
- Gerar vídeos no formato adequado (ex.: 9:16 para Reels/Shorts/TikTok)
- Usar APIs diferentes por plataforma
- Manter lógica separada para cada uma

## TikTok

### API

- **Nome**: Content Posting API
- **Docs**: https://developers.tiktok.com/doc/content-posting-api-get-started
- **Formato**: MP4, H.264, até 500MB

### Criar Conta/App

1. Acesse [TikTok for Developers](https://developers.tiktok.com/)
2. Crie conta e um app
3. Habilite o produto **Content Posting API**
4. Escopos necessários: `video.publish` (post direto) ou `video.upload` (draft)
5. Configure OAuth: redirect URL, permissões

### Keys/Credenciais

- **Client Key** e **Client Secret** do app
- **Access Token** por criador (obtido via OAuth)
- Usuário precisa autorizar o app

### Limitações

- Clientes não auditados: vídeos só em modo privado até aprovação
- ~60 requisições/minuto
- Processo de revisão para liberar post público

---

## Instagram

### API

- **Nome**: Instagram Graph API (Content Publishing)
- **Docs**: https://developers.facebook.com/docs/instagram-platform/content-publishing
- **Requisito**: Conta profissional/criador

### Criar Conta/App

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Crie um app
3. Adicione o produto **Instagram Graph API**
4. Níveis de acesso: **Standard** ou **Advanced**
5. Para publicar: precisa de **Page Publishing Authorization** em alguns casos

### Keys/Credenciais

- **App ID** e **App Secret**
- **Access Token** (página ou usuário Instagram)
- **Instagram Business/Creator Account ID**

### Fluxo de Publicação

1. Upload da mídia para um container (URL pública)
2. `POST /{ig-user-id}/media` com `media_type`, `video_url` etc.
3. `POST /{ig-user-id}/media_publish` com o `creation_id`

### Limitações

- Mídia deve estar em URL pública no momento da publicação
- ~50 posts/dia por conta
- Reels e Stories têm regras específicas

---

## Estrutura Futura (Separada)

```
youtube-content-automation/
├── uploaders/
│   ├── youtube_uploader.py   # atual
│   ├── tiktok_uploader.py    # futuro
│   └── instagram_uploader.py # futuro
├── config/
│   ├── youtube_credentials/
│   ├── tiktok_credentials/
│   └── instagram_credentials/
```

### Quando Implementar

1. Valide o pipeline completo no YouTube
2. Gere vídeos em 9:16 (Shorts) – já compatível com Reels/TikTok
3. Crie módulos de upload por plataforma
4. Adicione flags no `main.py`: `--platform youtube|tiktok|instagram|all`
