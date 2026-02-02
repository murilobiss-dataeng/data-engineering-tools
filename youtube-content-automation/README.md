# YouTube Content Automation - Múltiplos Canais

Gerador automático de shorts para YouTube com **múltiplos canais**: Salmo do Dia (150 salmos) e Passagem do Dia (passagens da Bíblia). Texto sincronizado com áudio e visual premium.

## Canais Disponíveis

| Canal | Conteúdo |
|-------|----------|
| **Salmo do Dia** | Livro de Salmos (150 salmos – Antigo Testamento). Shorts com salmos completos. |
| **Passagem do Dia** | Passagens da Bíblia: Evangelhos, Provérbios, Isaías, Romanos, Filipenses, etc. |

## Características

- **Múltiplos canais**: Escolha o canal com `--channel salmo_dia` ou `--channel passagem_do_dia`
- **Salmo do Dia**: Livro de Salmos com 150 salmos (Antigo Testamento); base com texto integral dos mais usados
- **Passagem do Dia**: Versículos e trechos de vários livros (João, Mateus, Provérbios, Isaías, etc.)
- **Texto sincronizado**: Cada página aparece enquanto está sendo narrada
- **Voz premium**: ElevenLabs em português
- **Visual profissional**: Gradientes, tipografia elegante, partículas de luz
- **Publicação multi-destino**: YouTube, Twitter/X, Kwai, Instagram, TikTok, Facebook, LinkedIn (cada um com credenciais opcionais)

## Requisitos

- Python 3.9+
- FFmpeg instalado
- API Key do ElevenLabs
- Credenciais dos destinos desejados (YouTube, Twitter, Kwai, IG, TikTok, Facebook, LinkedIn – opcional)

## Instalação

```bash
cd youtube-content-automation
pip install -r requirements.txt
cp .env.example .env
# Edite .env com suas API keys
```

## Uso

### Canal Salmo do Dia (padrão)

```bash
# Lista todos os salmos disponíveis
python main.py --channel salmo_dia --list

# Gera um salmo aleatório
python main.py --channel salmo_dia
# ou simplesmente (salmo_dia é o padrão):
python main.py

# Gera um salmo específico (índice 0 = Salmo 23)
python main.py --channel salmo_dia --index 0

# Gera e publica (todos os destinos configurados: YouTube, Twitter, Kwai, IG, etc.)
python main.py --channel salmo_dia --index 0 --publish

# Publica apenas em destinos específicos
python main.py --channel salmo_dia --publish --publish-to youtube,twitter,kwai,instagram
python main.py --channel salmo_dia --publish --publish-to all

# Ver informações de um salmo
python main.py --channel salmo_dia --info 3
```

### Canal Passagem do Dia

```bash
# Lista todas as passagens
python main.py --channel passagem_do_dia --list

# Gera uma passagem aleatória
python main.py --channel passagem_do_dia

# Gera passagem específica
python main.py --channel passagem_do_dia --index 0

# Gera e publica em vários destinos
python main.py --channel passagem_do_dia --publish --publish-to youtube,twitter,kwai,ig

# Ver informações de uma passagem
python main.py --channel passagem_do_dia --info 2
```

### Opções gerais

- `--channel`, `-c`: Canal (salmo_dia, passagem_do_dia). Padrão: salmo_dia
- `--list`, `-l`: Lista o conteúdo do canal
- `--index`, `-i`: Índice do item (use --list para ver índices)
- `--publish`, `-p`: Publica no Twitter/X após gerar
- `--output`, `-o`: Diretório de saída (padrão: outputs)
- `--info N`: Mostra informações do item de índice N

## Salmos (150 no livro)

O livro de Salmos na Bíblia tem **150 salmos** (cânticos/poemas), no Antigo Testamento, em cinco partes. O projeto inclui texto integral dos salmos mais utilizados; use `python main.py --channel salmo_dia --list` para ver a lista e o total com texto.

## Passagens da Bíblia

O canal Passagem do Dia usa versículos e trechos de:

- **Evangelhos**: João, Mateus, Lucas
- **Epístolas**: Romanos, Filipenses, 1 Coríntios, Efésios, Gálatas, Hebreus
- **Provérbios**, **Isaías**, **Jeremias**, **Josué**

Use `python main.py --channel passagem_do_dia --list` para ver todas.

## Estrutura do Projeto

```
youtube-content-automation/
├── main.py                    # Entrada multi-canal
├── config/
│   ├── channels.yaml          # Definição dos canais
│   └── templates_salmo_dia.yaml
├── channels/
│   ├── salmo_dia/             # Canal Salmo do Dia
│   └── passagem_do_dia/       # Canal Passagem do Dia
├── core/
│   ├── publishers/           # Publicação multi-destino
│   │   ├── youtube_publisher.py
│   │   ├── twitter_publisher.py
│   │   ├── kwai_publisher.py
│   │   ├── instagram_publisher.py
│   │   ├── tiktok_publisher.py
│   │   ├── facebook_publisher.py
│   │   ├── linkedin_publisher.py
│   │   └── dispatcher.py
│   ├── premium_visuals.py
│   ├── synced_video_generator.py
│   ├── text_to_speech_enhanced.py
│   └── twitter_publisher.py
├── data/
│   ├── salmos_completos.py    # 150 salmos (livro); texto integral dos principais
│   └── passagens_biblia.py    # Passagens de vários livros
├── outputs/
└── assets/fonts/
```

## Paletas Visuais

- **heavenly**: Dourados celestiais (paz, amor, gratidão)
- **sacred**: Azuis sagrados (proteção, verdade)
- **dawn**: Amanhecer (esperança, louvor, luz)
- **serene**: Verdes serenos (sabedoria, confiança)

## Licença

MIT
