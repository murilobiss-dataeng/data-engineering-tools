# Changelog

## [2026-01-26] - Atualizações Importantes

### ✅ Alterações Implementadas

1. **Vídeos Públicos por Padrão**
   - Todos os vídeos agora são enviados como `public` por padrão
   - Alterado em: `main.py`, `dags/*.py`, `core/youtube_uploader.py`

2. **Voz Melhorada para YouTube**
   - TTS agora usa `tld='com.br'` para voz brasileira mais natural
   - Velocidade normal (não lenta) para melhor qualidade
   - Aplicado em todos os canais

3. **Verificação de Duplicatas**
   - Sistema verifica se vídeo com mesmo título já existe
   - Se existir, não faz upload novamente
   - Retorna informações do vídeo existente

### 🔧 Detalhes Técnicos

#### Text-to-Speech
- **Antes:** `gTTS(lang='pt', slow=False)`
- **Agora:** `gTTS(lang='pt', slow=False, tld='com.br')`
- **Resultado:** Voz mais natural e adequada para YouTube

#### YouTube Upload
- **Antes:** Sempre fazia upload, mesmo se vídeo já existisse
- **Agora:** Verifica duplicatas antes de fazer upload
- **Método:** `video_exists(title)` busca no canal próprio

#### Privacidade
- **Antes:** `privacy_status='private'`
- **Agora:** `privacy_status='public'`
- **Aplicado em:** Todos os uploads

### 📝 Como Usar

```bash
# Gerar e fazer upload (verifica duplicatas automaticamente)
python main.py --channel explicado_shorts --upload
```

Se o vídeo já existir, você verá:
```
⚠️  Video já existe no YouTube
   Título: [título]
   URL: [url]
   Status: public
```

### 🎯 Benefícios

1. **Evita Duplicatas** - Não cria vídeos repetidos
2. **Voz Profissional** - Som mais adequado para YouTube
3. **Público por Padrão** - Vídeos já ficam disponíveis
