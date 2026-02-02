# Voz e Visual Profissionais

## Voz (TTS) - Gratuito

Ordem de prioridade (todos gratuitos):

1. **edge-tts** – Microsoft, boa qualidade (pode falhar 403 em alguns ambientes)
2. **Piper TTS** – Offline, modelo pt_BR baixado na primeira execução
3. **gTTS** – Google, sempre funciona

### Instalação

```bash
pip install edge-tts gtts pydub
# Opcional (offline): pip install piper-tts
```

### Piper TTS (opcional, offline)

Para usar Piper quando edge-tts falhar: `pip install piper-tts`. O modelo pt_BR é baixado automaticamente na primeira execução (~63 MB).

---

## Visual

### Unsplash (imagens reais)

1. Registre em https://unsplash.com/developers
2. Adicione em `config/api_keys.env`:
   ```
   UNSPLASH_ACCESS_KEY=sua_chave
   ```
3. O sistema usa a palavra-chave do conteúdo para buscar fotos

### Paletas de gradiente (quando não há Unsplash)

- `blue_pro` – Azul profissional
- `warm` – Tons quentes
- `nature` – Verde natureza
- `elegant` – Roxo elegante
- `energy` – Rosa/vermelho

### Tipografia

Templates atualizados com fontes maiores e contorno mais forte para legibilidade.
