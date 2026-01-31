# Como Individualizar o Caminho dos Canais para Uploads

## O Problema

O YouTube Data API v3 **não permite escolher o canal de destino** no upload. O vídeo sempre vai para o **canal padrão** da conta Google autenticada.

## Solução: Credenciais OAuth Separadas por Canal

Para enviar cada vídeo para o canal correto, você precisa de **uma conta Google por canal** (ou Brand Account vinculada a uma conta).

### Passo 1: Criar Projeto no Google Cloud (um por canal ou um com vários apps)

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto OU use o existente
3. Para cada canal:
   - Vá em **APIs e Serviços** → **Credenciais**
   - Crie credenciais **OAuth 2.0** (tipo "Aplicativo para computador")
   - Baixe o JSON e salve como:
     - `config/client_secrets_placar_dia.json`
     - `config/client_secrets_explicado_shorts.json`
     - `config/client_secrets_salmo_dia.json`
     - etc.

### Passo 2: Configurar youtube_channels.yaml

Edite `config/youtube_channels.yaml` e defina o `credentials_path` para cada canal:

```yaml
channels:
  placar_dia:
    name: "Placar do Dia"
    credentials_path: "config/client_secrets_placar_dia.json"
    category_id: "17"
    default_tags: ["futebol", "placar", ...]
    
  explicado_shorts:
    name: "Explicado em Shorts"
    credentials_path: "config/client_secrets_explicado_shorts.json"
    ...
```

### Passo 3: Autenticação Inicial

Na **primeira execução** de cada canal:
1. O sistema abrirá o navegador
2. **Faça login com a conta Google do canal correspondente**
3. Autorize o app
4. As credenciais serão salvas em `config/credentials_placar_dia.pickle` (por canal)

### Resumo Visual

```
Canal "Placar do Dia"  → client_secrets_placar.json    → Conta A (dona do canal)
Canal "Salmo do Dia"   → client_secrets_salmo.json     → Conta B (dona do canal)
Canal "Receita do Dia" → client_secrets_receita.json   → Conta C (dona do canal)
```

Cada conjunto de credenciais aponta para **um canal específico**.

### Brand Accounts (Opcional)

Se seus canais forem **Brand Accounts** gerenciados por uma conta principal:
- Use a conta principal para autenticar
- O YouTube pode permitir selecionar o canal na primeira vez
- Consulte a documentação do YouTube sobre Brand Accounts

## Implementação no Código

O `YouTubeUploader` deve ser inicializado com o caminho das credenciais do canal:

```python
# Em youtube_uploader.py - suporte a credentials_path por canal
uploader = YouTubeUploader(
    client_secrets_file=channel_config.get('credentials_path') or 'config/client_secrets.json'
)
```

O `main.py` já passa o `channel_name` para `upload_video`. O próximo passo é carregar o `credentials_path` do yaml e passar ao uploader.
