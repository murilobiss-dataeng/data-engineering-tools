# Leonardo AI para Imagens

## Sobre

O [Leonardo.ai](https://leonardo.ai) gera imagens por IA. É uma alternativa ao Nanobanana e similar.

## API

- **Docs**: https://docs.leonardo.ai/
- **Endpoint**: `POST https://cloud.leonardo.ai/api/rest/v1/generations`
- **Auth**: Bearer token (API Key)

### Obter API Key

1. Acesse [Leonardo.ai](https://leonardo.ai)
2. Crie conta e vá em **API** no menu
3. Gere uma API key
4. Adicione em `config/api_keys.env`:
   ```
   LEONARDO_API_KEY=sua_chave
   ```

### Uso Básico (Python)

```python
import requests
headers = {"Authorization": f"Bearer {LEONARDO_API_KEY}"}
payload = {
    "prompt": "Professional gradient background for video, blue tones",
    "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
    "width": 1920,
    "height": 1080
}
r = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations", headers=headers, json=payload)
# Usar generationId para buscar imagens geradas
```

### Integração no Projeto

O `core/image_processor.py` pode ganhar um método `generate_image_leonardo(prompt, size)` que:
1. Chama a API do Leonardo
2. Aguarda a geração
3. Baixa a imagem e salva localmente
4. Retorna o path para uso no vídeo

**Status**: Documentado. A implementação pode ser feita quando quiser usar imagens geradas por IA em vez de gradientes.
