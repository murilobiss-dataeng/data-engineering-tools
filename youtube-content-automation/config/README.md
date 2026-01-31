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
- `templates_explicado_shorts.yaml`
- `templates_quanto_rende.yaml`
- `templates_series_explicadas.yaml`

### client_secrets.json
**⚠️ NÃO COMMITAR** - Credenciais OAuth2 do YouTube.
- Baixado do Google Cloud Console
- Contém informações sensíveis

### credentials.pickle / credentials_*.pickle
**⚠️ NÃO COMMITAR** - Tokens de acesso do YouTube.
- Criado automaticamente após primeira autorização
- Não editar manualmente

### Arquivos por canal (placar_do_dia, quanto_rende, etc.)
**⚠️ NÃO COMMITAR** - Credenciais OAuth por canal.
- Contêm client_id e client_secret do Google
- Usados para upload em canais separados

## Segurança

Todos os arquivos sensíveis estão no `.gitignore`:
- `api_keys.env`
- `client_secrets*.json`
- `credentials*.pickle`
- `placar_do_dia`, `quanto_rende`, `series_explicadas`, etc.

**Antes de `git add`:** verifique que nenhum arquivo com credenciais será commitado.
