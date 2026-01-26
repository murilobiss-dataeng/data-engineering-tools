# Guia de Instalação

## Ambiente Virtual

O projeto usa um ambiente virtual isolado para gerenciar dependências.

## Instalação Automática

Execute o script de instalação:

```bash
./install_dependencies.sh
```

Este script irá:
1. Criar o ambiente virtual (se não existir)
2. Ativar o ambiente virtual
3. Atualizar pip, setuptools e wheel
4. Instalar todas as dependências do `requirements.txt`

## Instalação Manual

### 1. Criar Ambiente Virtual

```bash
python3 -m venv venv
```

### 2. Ativar Ambiente Virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Atualizar pip

```bash
pip install --upgrade pip setuptools wheel
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

## Verificar Instalação

Após instalar, teste se tudo está funcionando:

```bash
# Com o venv ativado
python tests/test_imports.py
```

## Usar o Ambiente Virtual

Sempre que for trabalhar no projeto:

1. **Ativar o ambiente:**
   ```bash
   source venv/bin/activate
   ```
   Você verá `(venv)` no início da linha do terminal.

2. **Executar comandos:**
   ```bash
   python main.py --channel explicado_shorts
   ```

3. **Desativar quando terminar:**
   ```bash
   deactivate
   ```

## Dependências Principais

- **moviepy** - Geração e edição de vídeos
- **Pillow** - Processamento de imagens
- **gtts** - Text-to-Speech
- **google-api-python-client** - YouTube Data API
- **requests** - Requisições HTTP
- **pyyaml** - Leitura de arquivos YAML
- **pandas** - Manipulação de dados
- **matplotlib** - Gráficos e visualizações

Ver `requirements.txt` para lista completa.

## Solução de Problemas

### Erro: "No module named 'moviepy'"
- Certifique-se de que o ambiente virtual está ativado
- Execute: `pip install -r requirements.txt`

### Erro: "pip: command not found"
- Instale pip: `python3 -m ensurepip --upgrade`
- Ou use: `python3 -m pip install -r requirements.txt`

### Erro de conexão ao instalar
- Verifique sua conexão com a internet
- Alguns pacotes podem demorar para baixar

### FFmpeg não encontrado
- Instale FFmpeg separadamente (necessário para MoviePy)
- Ver `docs/INSTALL_FFMPEG.md`

## Status Atual

✅ Ambiente virtual criado em `venv/`
⚠️ Dependências precisam ser instaladas (requer conexão com internet)
