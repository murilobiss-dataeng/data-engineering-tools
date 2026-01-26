# Configurações

Esta pasta contém todos os arquivos de configuração do sistema.

## Arquivos

### api_keys.env
**⚠️ NÃO COMMITAR** - Contém chaves de API sensíveis.
- Copie de `api_keys.env.example`
- Preencha com suas chaves reais

### api_keys.env.example
Template de exemplo para as chaves de API.

### channels.yaml
Configurações específicas de cada canal:
- IDs de ligas
- Frequência de publicação
- Configurações de conteúdo

### templates.yaml
Templates padrão de vídeo (shorts e long-form).

### templates_*.yaml
Templates específicos por canal:
- `templates_placar_dia.yaml`
- `templates_bets_dia.yaml`
- `templates_explicado_shorts.yaml`
- `templates_quanto_rende.yaml`
- `templates_series_explicadas.yaml`

### client_secrets.json
**⚠️ NÃO COMMITAR** - Credenciais OAuth2 do YouTube.
- Baixado do Google Cloud Console
- Contém informações sensíveis

### credentials.pickle
**⚠️ NÃO COMMITAR** - Tokens de acesso do YouTube.
- Criado automaticamente após primeira autorização
- Não editar manualmente

## Segurança

Todos os arquivos sensíveis estão no `.gitignore`:
- `api_keys.env`
- `client_secrets.json`
- `credentials.pickle`
