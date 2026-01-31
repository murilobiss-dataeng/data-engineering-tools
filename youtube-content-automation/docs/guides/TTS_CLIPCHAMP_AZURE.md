# Voz no Estilo Clipchamp (Azure Speech)

## Sobre Clipchamp

O Clipchamp usa **Microsoft Azure AI Speech** para gerar vozes. O Clipchamp em si **não possui API** – é um app desktop/web. Para automação, use diretamente o **Azure Speech Services**.

## Azure Speech Services

- **Qualidade**: Neural TTS, vozes naturais em PT-BR
- **Custo**: Cobrança por caractere (ex.: ~US$4/milhão caracteres)
- **API**: REST e SDK Python disponíveis

### Configuração

1. Crie uma conta no [Azure](https://azure.microsoft.com/)
2. Crie um recurso **Speech** no portal
3. Copie **Region** e **Key**
4. Adicione em `config/api_keys.env`:
   ```
   AZURE_SPEECH_KEY=sua_chave
   AZURE_SPEECH_REGION=brazilsouth
   ```

### Uso no Projeto

O módulo `core/text_to_speech_azure.py` (a ser criado) pode usar:

```python
import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
result = synthesizer.speak_text_async(text).get()
```

### Alternativas Gratuitas/Similares

| Serviço        | Qualidade | API | Custo              |
|----------------|-----------|-----|--------------------|
| edge-tts       | Boa       | Sim | Gratuito           |
| Azure Speech   | Muito boa | Sim | Pago por caractere |
| ElevenLabs     | Muito boa | Sim | Pago               |
| gTTS           | Básica    | Sim | Gratuito           |

**Recomendação**: Se edge-tts falhar (403), o sistema já usa gTTS como fallback. Para voz no nível Clipchamp, integre Azure Speech quando quiser investir em qualidade.
