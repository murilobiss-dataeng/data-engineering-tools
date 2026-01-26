# Atualizações Recentes

## ✅ Implementado em 26/01/2026

### 1. Vídeos Públicos por Padrão
- ✅ Todos os uploads agora são `public` por padrão
- ✅ Alterado em todos os DAGs e no `main.py`
- ✅ Não precisa mais editar código para tornar público

### 2. Voz Melhorada para YouTube
- ✅ TTS usa `tld='com.br'` para voz brasileira mais natural
- ✅ Velocidade normal (não lenta) para melhor qualidade
- ✅ Aplicado em todos os 5 canais

**Antes:**
```python
TextToSpeech(output_dir)  # Voz padrão
```

**Agora:**
```python
TextToSpeech(output_dir, language='pt', slow=False, tld='com.br')  # Voz brasileira melhorada
```

### 3. Verificação de Duplicatas
- ✅ Sistema verifica se vídeo já existe antes de fazer upload
- ✅ Busca por título exato no seu canal
- ✅ Se existir, mostra informações e não faz upload novamente

**Como funciona:**
```python
# Verifica automaticamente antes de fazer upload
uploader.upload_video(
    ...,
    check_duplicate=True  # Padrão: True
)
```

**Se vídeo já existir:**
```
⚠️  Video já existe no YouTube
   Título: [título]
   URL: https://www.youtube.com/watch?v=...
   Status: public
```

## 🎯 Resultado

Agora quando você executar:
```bash
python main.py --channel explicado_shorts --upload
```

O sistema irá:
1. ✅ Gerar vídeos com voz melhorada
2. ✅ Verificar se já existe no YouTube
3. ✅ Fazer upload apenas se não existir
4. ✅ Publicar como público automaticamente

## 📝 Notas

- A verificação de duplicatas busca apenas no seu próprio canal
- Compara títulos exatos (case-sensitive)
- Se quiser forçar upload mesmo com duplicata, use `check_duplicate=False`
