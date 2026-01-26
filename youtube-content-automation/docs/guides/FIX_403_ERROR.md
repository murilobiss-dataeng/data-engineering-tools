# Como Resolver Erro 403: access_denied

## 🔴 Problema

```
Erro 403: access_denied
ConteudoHub.iss não concluiu o processo de verificação do Google.
Ele está em fase de testes e só pode ser acessado por testadores aprovados.
```

## ✅ Solução Passo a Passo

### Passo 1: Acessar Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Selecione o projeto: `flowing-code-485516-j3` (ou seu projeto)

### Passo 2: Configurar Tela de Consentimento OAuth

1. No menu lateral, vá em **"APIs e Serviços"** > **"Tela de consentimento OAuth"**
2. Você verá que está como **"Em teste"**

**Opção A: Adicionar Usuários de Teste (Rápido)**

1. Na seção **"Usuários de teste"**, clique em **"+ ADICIONAR USUÁRIOS"**
2. Adicione seu email (o mesmo que usa no YouTube)
3. Clique em **"Adicionar"**
4. Agora você poderá autorizar o app

**Opção B: Publicar o App (Recomendado para Produção)**

1. Na parte superior da página, clique em **"PUBLICAR APP"**
2. Confirme a publicação
3. **Atenção:** Isso pode levar alguns dias para ser aprovado pelo Google
4. Enquanto isso, use a Opção A

### Passo 3: Verificar Configurações

Certifique-se de que:

1. **Tipo de usuário:** "Externo" (para uso pessoal)
2. **Escopos:** Deve incluir `https://www.googleapis.com/auth/youtube.upload`
3. **Usuários de teste:** Seu email está listado

### Passo 4: Testar Novamente

Após adicionar seu email como testador:

1. Tente fazer upload novamente:
   ```bash
   python main.py --channel explicado_shorts --upload
   ```

2. Na primeira vez, o navegador abrirá
3. Você verá uma tela de aviso dizendo que o app não está verificado
4. Clique em **"Avançar"** ou **"Continuar"**
5. Autorize o acesso

## 🔧 Configuração Detalhada

### Adicionar Múltiplos Usuários de Teste

Se você tem múltiplas contas ou quer adicionar outros emails:

1. Vá em **"Tela de consentimento OAuth"**
2. Seção **"Usuários de teste"**
3. Clique em **"+ ADICIONAR USUÁRIOS"**
4. Adicione todos os emails necessários (separados por vírgula)
5. Salve

### Verificar Escopos Necessários

Os escopos necessários são:
- `https://www.googleapis.com/auth/youtube.upload` - Upload de vídeos
- `https://www.googleapis.com/auth/youtube.readonly` - Ler informações (para verificar duplicatas)

Estes devem estar configurados automaticamente quando você cria as credenciais OAuth.

## ⚠️ Importante

- **App em Teste:** Funciona apenas para usuários adicionados como testadores
- **Limite:** Máximo de 100 usuários de teste
- **Produção:** Para uso público, precisa publicar o app (pode levar dias)

## 🎯 Solução Rápida

**Para resolver AGORA:**

1. Acesse: https://console.cloud.google.com/apis/credentials/consent
2. Selecione seu projeto
3. Clique em **"+ ADICIONAR USUÁRIOS"** na seção "Usuários de teste"
4. Adicione seu email
5. Salve
6. Tente novamente o upload

## 📝 Checklist

- [ ] Email adicionado como usuário de teste
- [ ] Tela de consentimento configurada
- [ ] Escopos corretos (youtube.upload e youtube.readonly)
- [ ] Credenciais OAuth criadas
- [ ] `client_secrets.json` no lugar correto

## 🆘 Ainda com Problemas?

Se ainda não funcionar:

1. **Verifique o email:** Use exatamente o mesmo email da conta do YouTube
2. **Aguarde alguns minutos:** Mudanças podem levar alguns minutos para propagar
3. **Limpe credenciais antigas:** Delete `config/credentials.pickle` e tente novamente
4. **Verifique permissões:** Certifique-se de que a conta tem acesso aos canais do YouTube
