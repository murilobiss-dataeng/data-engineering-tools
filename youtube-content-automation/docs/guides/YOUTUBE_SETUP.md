# Configuração do YouTube API

## 📍 Link Direto

**Google Cloud Console:** https://console.cloud.google.com/

## ✅ Status

As credenciais já estão configuradas em `config/client_secrets.json`.

## Primeira Autorização

Na primeira execução com `--upload`:

1. O script abrirá automaticamente seu navegador
2. Faça login com a conta do YouTube que gerencia seus canais
3. Clique em **"Permitir"** ou **"Allow"** para autorizar o acesso
4. As credenciais serão salvas automaticamente em `config/credentials.pickle`
5. Nas próximas execuções, não precisará autorizar novamente

## 🧪 Testar

```bash
# Gerar vídeo sem upload
python main.py --channel explicado_shorts

# Gerar e fazer upload (primeira vez abrirá navegador)
python main.py --channel explicado_shorts --upload
```

## ⚠️ Importante

- ✅ Use a mesma conta Google que gerencia seus 5 canais do YouTube
- ✅ O arquivo `client_secrets.json` é sensível - não compartilhe
- ✅ O arquivo `credentials.pickle` será criado automaticamente após primeira autorização
- ✅ Uma vez autorizado, não precisará autorizar novamente

## 🔴 Erro 403: access_denied?

Se você receber o erro "403: access_denied" ou "app está em fase de testes":

1. **Adicione seu email como usuário de teste:**
   - Acesse: https://console.cloud.google.com/apis/credentials/consent
   - Selecione seu projeto
   - Na seção "Usuários de teste", clique em "+ ADICIONAR USUÁRIOS"
   - Adicione o email da sua conta do YouTube
   - Salve

2. **Aguarde alguns minutos** para as mudanças propagarem

3. **Tente novamente** o upload

Ver guia completo em: `docs/guides/FIX_403_ERROR.md`

## 📞 Problemas Comuns

**Erro: "FileNotFoundError: client_secrets.json"**
- Verifique se o arquivo está em `config/client_secrets.json`

**Erro: "Access blocked: This app's request is invalid"**
- Verifique se adicionou seu email como "Usuário de teste" na tela de consentimento
- Aguarde alguns minutos após criar as credenciais
