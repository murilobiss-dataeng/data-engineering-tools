# Testes

Esta pasta contém os scripts de teste para verificar as integrações com as APIs.

## Testes Disponíveis

### test_football_api.py
Testa a integração com a API-Football:
- Conexão com a API
- Busca de ligas brasileiras
- Busca de jogos do dia
- Busca de classificação

**Uso:**
```bash
python tests/test_football_api.py
```

### test_tmdb_api.py
Testa a integração com a TMDB API:
- Conexão com a API
- Busca de séries de TV
- Detalhes de séries
- Imagens e posters

**Uso:**
```bash
python tests/test_tmdb_api.py
```

## Executar Todos os Testes

```bash
python tests/test_football_api.py && python tests/test_tmdb_api.py
```
