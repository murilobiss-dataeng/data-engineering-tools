# Segurança e Proteção de Credenciais

## Arquivos Sensíveis (já no .gitignore)

| Arquivo | Conteúdo | Risco |
|---------|----------|-------|
| `config/api_keys.env` | Chaves API-Football, TMDB, etc. | Alto – uso não autorizado das APIs |
| `config/client_secrets*.json` | OAuth Google (client_id, client_secret) | Crítico – acesso à conta YouTube |
| `config/credentials*.pickle` | Tokens de acesso OAuth | Crítico – upload sem re-autenticação |
| `config/placar_do_dia`, `config/quanto_rende`, etc. | OAuth por canal | Crítico – credenciais por canal |

## Verificação Antes de Commitar

```bash
# Nunca commitar arquivos com credenciais
git status
# Se aparecer api_keys.env, client_secrets*.json, credentials*.pickle ou
# config/placar_do_dia etc., NÃO adicione ao commit
```

## Recomendações

1. **Revogue e recrie** chaves se qualquer credencial tiver sido commitada no passado
2. **Não compartilhe** `api_keys.env` ou arquivos `config/*` com credenciais
3. **Use variáveis de ambiente** em CI/CD em vez de arquivos
4. **Rotacione** chaves periodicamente

## Localização das Configs

Todas as configurações ficam em:

```
/home/crislaine/GitProjects/data-engineering-tools/youtube-content-automation/config/
```

O código resolve paths relativamente à raiz do projeto (`PROJECT_ROOT`).
