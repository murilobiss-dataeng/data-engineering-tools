# Solução de Problemas

## Problema: ImageMagick não encontrado

### Erro
```
OSError: MoviePy Error: creation of None failed because of the following error:
[Errno 20] Not a directory: 'unset'.
This error can be due to the fact that ImageMagick is not installed...
```

### Solução Implementada

O código foi modificado para **não usar ImageMagick**. Agora usa **PIL/Pillow diretamente** para criar imagens de texto, que são então convertidas para clips de vídeo.

### Como Funciona Agora

1. **Texto é renderizado usando PIL** - Cria imagens PNG/RGBA com o texto
2. **Imagens são convertidas para numpy arrays** - Compatível com MoviePy
3. **ImageClip é criado** - Sem necessidade de ImageMagick

### Vantagens

- ✅ Não requer ImageMagick
- ✅ Mais rápido
- ✅ Mais controle sobre o texto
- ✅ Suporte a word wrapping automático

## Outros Problemas Comuns

### FFmpeg não encontrado

**Erro:** `ffmpeg: command not found`

**Solução:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

Ou siga o guia em `docs/INSTALL_FFMPEG.md`

### Módulos não encontrados

**Erro:** `ModuleNotFoundError: No module named 'X'`

**Solução:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Erro de conexão com APIs

**Erro:** `ConnectionError` ou `Name or service not known`

**Solução:**
- Verifique sua conexão com a internet
- Verifique se as chaves de API estão corretas em `config/api_keys.env`

### Erro ao fazer upload para YouTube

**Erro:** `FileNotFoundError: client_secrets.json`

**Solução:**
- Verifique se o arquivo `config/client_secrets.json` existe
- Siga o guia em `docs/guides/YOUTUBE_SETUP.md`

## Testes

Para verificar se tudo está funcionando:

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Testar imports
python tests/test_imports.py

# Testar APIs (requer internet)
python tests/test_football_api.py
python tests/test_tmdb_api.py

# Testar geração de vídeo
python main.py --channel explicado_shorts
```
