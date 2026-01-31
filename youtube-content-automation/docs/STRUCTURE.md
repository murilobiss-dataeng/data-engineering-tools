# 📁 Estrutura do Projeto

```
youtube-content-automation/
│
├── 📂 channels/              # Módulos específicos por canal
│   ├── placar_dia/          # Resumos de jogos
│   ├── explicado_shorts/    # Vídeos educacionais
│   ├── quanto_rende/        # Simulações financeiras
│   └── series_explicadas/   # Resumos de séries
│
├── 📂 core/                  # Componentes compartilhados
│   ├── video_generator.py   # Geração de vídeos
│   ├── template_engine.py  # Sistema de templates
│   ├── text_to_speech.py    # Narração automática
│   ├── youtube_uploader.py # Upload para YouTube
│   └── image_processor.py   # Processamento de imagens
│
├── 📂 data_sources/          # Integrações com APIs
│   ├── football_api.py      # API-Football
│   ├── tmdb_api.py          # The Movie Database
│   ├── financial_api.py     # Dados financeiros
│   └── content_generator.py # Geração de conteúdo
│
├── 📂 config/                # Configurações
│   ├── api_keys.env         # Chaves de API (não commitado)
│   ├── channels.yaml        # Config dos canais
│   ├── templates*.yaml      # Templates de vídeo
│   └── client_secrets.json  # Credenciais YouTube (não commitado)
│
├── 📂 tests/                 # Testes
│   ├── test_football_api.py
│   └── test_tmdb_api.py
│
├── 📂 docs/                  # Documentação
│   ├── guides/              # Guias de configuração
│   ├── CHECKLIST_CONFIGURACAO.md
│   ├── STATUS.md
│   ├── EXAMPLES.md
│   └── INSTALL_FFMPEG.md
│
├── 📂 dags/                  # Airflow DAGs
│   ├── placar_dia_dag.py
│   └── content_scheduler_dag.py
│
├── 📂 outputs/               # Vídeos gerados
│   ├── shorts/
│   └── long_form/
│
├── 📄 main.py                # Entry point
├── 📄 requirements.txt       # Dependências
└── 📄 README.md             # Documentação principal
```

## 🎯 Organização

### ✅ Testes
- Todos os testes em `tests/`
- Scripts de teste organizados por API

### ✅ Documentação
- Toda documentação em `docs/`
- Guias em `docs/guides/`
- READMEs em cada pasta importante

### ✅ Configurações
- Todas as configs em `config/`
- Valores não hardcoded
- Uso de variáveis de ambiente e YAML

### ✅ Segurança
- Arquivos sensíveis no `.gitignore`
- Templates de exemplo fornecidos
- Credenciais não commitadas

## 🔒 Arquivos Sensíveis (não commitados)

- `config/api_keys.env`
- `config/client_secrets.json`
- `config/credentials.pickle`

## 📝 Arquivos de Exemplo

- `config/api_keys.env.example`
- Templates YAML com valores padrão
