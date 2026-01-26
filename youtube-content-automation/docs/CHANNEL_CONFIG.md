# Configuração de Canais do YouTube

## ⚠️ Importante sobre Múltiplos Canais

O YouTube Data API v3 **não permite especificar diretamente qual canal usar** no upload. O vídeo sempre vai para o **canal padrão** da conta autenticada.

## Soluções Possíveis

### Opção 1: Múltiplas Contas OAuth (Recomendado)

Para ter controle total sobre qual canal recebe cada vídeo:

1. **Crie credenciais OAuth separadas** para cada canal
2. **Salve cada `client_secrets.json`** com nome diferente:
   - `config/client_secrets_placar_dia.json`
   - `config/client_secrets_explicado_shorts.json`
   - etc.

3. **Modifique o código** para usar credenciais diferentes por canal

### Opção 2: Brand Accounts (Avançado)

Se seus canais estão em Brand Accounts:
- Configure Brand Accounts no YouTube
- Use a conta principal para gerenciar todos
- O sistema pode ser adaptado para isso

### Opção 3: Usar Canal Padrão (Atual)

**Como funciona agora:**
- Todos os vídeos vão para o canal padrão da conta autenticada
- O sistema identifica o tipo de conteúdo via `channel_name`
- Tags e categorias são ajustadas por canal
- **Mas o vídeo físico vai para o canal padrão**

## Configuração Atual

O arquivo `config/youtube_channels.yaml` permite:
- Configurar categoria por canal
- Configurar tags padrão por canal
- Preparar para futura implementação de múltiplos canais

## Verificar Canal Padrão

Para ver qual é seu canal padrão:

1. Acesse: https://studio.youtube.com/
2. O canal mostrado no topo é o padrão
3. Todos os uploads vão para este canal

## Solução Temporária

**Se você precisa que vídeos vão para canais diferentes:**

1. Use contas Google diferentes para cada canal
2. Crie `client_secrets.json` separados
3. Execute o sistema com credenciais diferentes por canal

Ou aguarde implementação futura de suporte a Brand Accounts.
