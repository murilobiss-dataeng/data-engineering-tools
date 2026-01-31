# CapCut para Edição

## Sobre

O CapCut (ByteDance) é um editor de vídeo. Existe um **CapCut API** não-oficial que permite automatizar a edição.

## CapCut API (Não-oficial)

- **Repositório**: https://github.com/renqingfei/CapCutAPI
- **Docs**: https://capcutapi.apifox.cn/
- **Funcionalidade**: Criar drafts, adicionar assets, aplicar efeitos via HTTP

### Limitações

- Não é API oficial do CapCut
- Pode quebrar com atualizações do app
- Requer o CapCut (Jianying) instalado localmente em alguns fluxos

### Alternativa: MoviePy (Atual)

O projeto **já usa MoviePy** para edição programática:
- Geração de vídeo
- Overlay de texto
- Áudio + imagens

Para migrar para CapCut:
1. Instale e configure o CapCut API
2. Crie um módulo `core/capcut_editor.py` que:
   - Cria drafts
   - Adiciona mídia (imagens, áudio)
   - Aplica transições
   - Exporta o vídeo
3. Use como opção em vez do MoviePy no pipeline

**Recomendação**: Valide primeiro o fluxo completo com MoviePy no YouTube. Depois avalie CapCut se precisar de edições mais avançadas (transições, efeitos específicos do CapCut).
