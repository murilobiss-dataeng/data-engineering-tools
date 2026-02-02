# Curriculum Vitae

Gerador de sites de currículo profissional. Cada pessoa tem sua própria pasta com arquivos independentes.

## Estrutura

```
curriculum-vitae/
├── README.md           # Este arquivo (documentação geral)
├── nathan/             # Currículo do Nathan
│   ├── index.html
│   ├── cv.html
│   ├── styles.css
│   ├── script.js
│   ├── resume.json
│   └── ...
├── [outra-pessoa]/     # Criar pasta para cada novo currículo
│   └── ...
```

## Como criar um novo currículo

### 1. Copie uma pasta existente

```bash
cp -r nathan/ nome-da-pessoa/
```

### 2. Edite o `resume.json`

Atualize todos os dados pessoais:

```json
{
  "name": "Nome Completo",
  "title": "Título Profissional",
  "tagline": "Descrição breve",
  "photo": "perfil.jpeg",
  "contact": {
    "address": "Cidade, Estado",
    "phone": "(00) 0 0000-0000",
    "email": "email@exemplo.com",
    "linkedin": "https://linkedin.com/in/perfil",
    "whatsapp": "5500000000000"
  },
  "experience": [...],
  "education": [...],
  "skills": [...],
  "languages": [...],
  "atsKeywords": [...]
}
```

### 3. Adicione a foto

Coloque a foto de perfil na pasta com o nome definido em `resume.json`.

### 4. Rodar localmente

```bash
cd nome-da-pessoa
python3 -m http.server 3000
```

Acesse: http://localhost:3000

### 5. Deploy no Vercel

Configure o **Root Directory** como `curriculum-vitae/nome-da-pessoa`.

## Funcionalidades

- Site responsivo com design moderno
- Dados carregados dinamicamente via JSON
- Página de CV para impressão/PDF (`cv.html`)
- Otimizado para ATS (palavras-chave)
- Cards de contato (WhatsApp, Email, LinkedIn)
- Seção de idiomas
- Compatível com Vercel

## Personalização

- **Cores**: Edite as variáveis CSS em `styles.css`
- **Fontes**: Altere o link do Google Fonts em `index.html`
- **Seções**: Adicione campos no JSON conforme necessário

## Currículos disponíveis

| Pessoa | Pasta | Status |
|--------|-------|--------|
| Nathan de Souza | `nathan/` | Ativo |
