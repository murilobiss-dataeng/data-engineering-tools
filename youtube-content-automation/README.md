# 🎬 Automação de Conteúdo para YouTube

Sistema profissional automatizado para criação e upload de conteúdo para 10 canais do YouTube.

## 📺 Canais

1. **Placar do Dia** - Resumos de jogos da rodada
2. **Explicado em Shorts** - Vídeos educacionais curtos
3. **Quanto rende?** - Simulações de rendimento financeiro
4. **Series Explicadas** - Resumos de séries sem spoilers
5. **Salmo do Dia** - Reflexão diária com salmos
6. **Receita do Dia** - Culinária e receitas
7. **Exercício do Dia** - Fitness e bem-estar
8. **Motivação do Dia** - Desenvolvimento pessoal
9. **Curiosidade do Dia** - Top 10 e curiosidades
10. **Dica de Carreira do Dia** - Dicas profissionais

## ✨ Características

- 🎙️ **Voz Profissional**: TTS neural de alta qualidade (edge-tts)
- 🎨 **Visual Profissional**: Backgrounds com gradientes e texturas
- 📝 **Conteúdo Robusto**: Explicações detalhadas e educativas
- 🎯 **Canal Correto**: Cada vídeo vai para o canal apropriado
- ✅ **Verificação de Duplicatas**: Não faz upload de vídeos repetidos
- 🌐 **Público por Padrão**: Vídeos publicados automaticamente

## 🚀 Instalação

```bash
# 1. Clone o repositório
git clone <repo-url>
cd youtube-content-automation

# 2. Execute o script de instalação
./scripts/install.sh

# 3. Configure as APIs (ver docs/guides/)
```

## 📖 Uso

### Gerar e Fazer Upload

```bash
source venv/bin/activate

# Explicado em Shorts
python main.py --channel explicado_shorts --upload

# Placar do Dia
python main.py --channel placar_dia --upload

# Outros canais
python main.py --channel quanto_rende --upload
python main.py --channel series_explicadas --upload
python main.py --channel salmo_dia --upload
python main.py --channel receita_dia --upload
python main.py --channel exercicio_dia --upload
python main.py --channel motivacao_dia --upload
python main.py --channel curiosidade_dia --upload
python main.py --channel dica_carreira_dia --upload
```

### Apenas Gerar (sem upload)

```bash
python main.py --channel explicado_shorts
```

## 🏗️ Estrutura

```
youtube-content-automation/
├── channels/          # Módulos por canal
├── core/              # Componentes core (vídeo, TTS, upload)
├── data_sources/      # Integrações com APIs
├── config/            # Configurações (canais, templates)
├── tests/             # Testes automatizados
├── docs/              # Documentação completa
├── scripts/           # Scripts de instalação
├── dags/              # Airflow DAGs
└── outputs/           # Vídeos gerados
```

## ⚙️ Configuração

### APIs Necessárias

1. **API-Football** - Já configurada
2. **TMDB API** - Já configurada
3. **YouTube Data API v3** - Já configurada

### Primeira Execução

Na primeira vez com `--upload`:
1. Navegador abrirá automaticamente
2. Faça login com conta do YouTube
3. Autorize o acesso
4. Credenciais serão salvas automaticamente

**Importante:** Adicione seu email como "Usuário de teste" no Google Cloud Console se receber erro 403.

## 📚 Documentação

Toda documentação está em `docs/`:

- `docs/guides/YOUTUBE_SETUP.md` - Configuração do YouTube
- `docs/guides/FIX_403_ERROR.md` - Resolver erro 403
- `docs/guides/CANAIS_INDIVIDUAIS.md` - Upload em canais separados
- `docs/guides/TTS_CLIPCHAMP_AZURE.md` - Voz Azure (estilo Clipchamp)
- `docs/guides/LEONARDO_IMAGENS.md` - Imagens com Leonardo AI
- `docs/guides/CAPCUT_EDICAO.md` - Edição com CapCut
- `docs/MULTI_PLATFORM_TIKTOK_IG.md` - TikTok e Instagram (futuro)
- `docs/INSTALLATION.md` - Guia de instalação
- `docs/USAGE.md` - Guia de uso
- `docs/IMPROVEMENTS.md` - Melhorias implementadas

## 🧪 Testes

```bash
source venv/bin/activate

# Testar imports
python tests/test_imports.py

# Testar APIs (requer internet)
python tests/test_football_api.py
python tests/test_tmdb_api.py
```

## 🔧 Requisitos

- Python 3.9+
- FFmpeg
- Chaves de API (já configuradas)

## 📝 Licença

MIT
