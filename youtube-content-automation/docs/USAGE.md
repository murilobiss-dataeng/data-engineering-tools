# Guia de Uso

## Gerar Vídeos

### Gerar sem Upload

Para apenas gerar os vídeos localmente (sem enviar para YouTube):

```bash
source venv/bin/activate
python main.py --channel explicado_shorts
```

Os vídeos serão salvos em `outputs/`:
- Shorts: `outputs/explicado_short_*.mp4`
- Long-form: `outputs/explicado_long_*.mp4`

### Gerar e Fazer Upload

Para gerar os vídeos **E** enviar para o YouTube:

```bash
source venv/bin/activate
python main.py --channel explicado_shorts --upload
```

**Na primeira vez:**
- Um navegador será aberto automaticamente
- Faça login com sua conta do YouTube
- Autorize o acesso
- As credenciais serão salvas automaticamente

**Nas próximas vezes:**
- O upload será feito automaticamente sem precisar autorizar novamente

## Canais Disponíveis

```bash
# Placar do Dia - Resumos de jogos
python main.py --channel placar_dia --upload

# Explicado em Shorts - Vídeos educacionais
python main.py --channel explicado_shorts --upload

# Quanto rende? - Simulações financeiras
python main.py --channel quanto_rende --upload

# Series Explicadas - Resumos de séries
python main.py --channel series_explicadas --upload
```

## Upload de Vídeos Existentes

Se você já tem vídeos gerados e quer fazer upload:

```python
from core.youtube_uploader import YouTubeUploader

uploader = YouTubeUploader()
uploader.upload_video(
    video_path="outputs/seu_video.mp4",
    title="Título do Vídeo",
    description="Descrição do vídeo",
    tags=["tag1", "tag2", "tag3"],
    privacy_status="private"  # ou "public" ou "unlisted"
)
```

## Configurações de Privacidade

No código, os vídeos são enviados como `private` por padrão. Para mudar:

1. Edite `main.py` na função `upload_video()`
2. Altere `privacy_status='private'` para:
   - `'public'` - Público (qualquer um pode ver)
   - `'unlisted'` - Não listado (só quem tem o link)
   - `'private'` - Privado (só você)

## Verificar Vídeos Gerados

```bash
# Listar vídeos gerados
ls -lh outputs/*.mp4

# Ver tamanho dos arquivos
du -sh outputs/
```

## Troubleshooting

### Vídeo gerado mas não enviado

**Problema:** Vídeo foi gerado mas não apareceu no YouTube

**Solução:** Use a flag `--upload`:
```bash
python main.py --channel explicado_shorts --upload
```

### Erro na primeira autorização

**Problema:** Navegador não abre ou erro de autorização

**Solução:**
1. Verifique se `config/client_secrets.json` existe
2. Verifique se está usando a conta correta do YouTube
3. Tente novamente

### Vídeos muito grandes

**Problema:** Upload demora muito ou falha

**Solução:**
- Vídeos longos podem demorar para fazer upload
- Verifique sua conexão com a internet
- O YouTube tem limite de tamanho (128GB ou 12 horas)
