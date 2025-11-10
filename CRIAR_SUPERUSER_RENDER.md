# 🔑 Como Criar Superusuário no Render (Plano Free)

O plano Free do Render não oferece acesso ao Shell. Aqui estão **3 soluções** para criar seu superusuário:

---

## ✅ Solução 1: Automática via Build Script (IMPLEMENTADA)

### Como Funciona

Criei um comando Django personalizado que roda automaticamente durante o deploy e cria o superusuário se ele não existir.

### Credenciais Padrão

Por padrão, será criado:

- **Username**: `admin`
- **Email**: `admin@biblioteca.com`
- **Password**: `admin123456`

⚠️ **IMPORTANTE**: Troque essa senha após o primeiro login!

### Como Aplicar

```powershell
# 1. Commitar as mudanças
git add .
git commit -m "Adicionar criação automática de superusuário"

# 2. Push para o GitHub
git push origin main

# 3. O Render faz deploy automático
# O superusuário será criado automaticamente!
```

### Personalizar Credenciais

Se quiser usar outras credenciais, adicione variáveis de ambiente no Render:

**Dashboard → Settings → Environment → Add Environment Variable:**

```
DJANGO_SUPERUSER_USERNAME=seu_username
DJANGO_SUPERUSER_EMAIL=seu@email.com
DJANGO_SUPERUSER_PASSWORD=sua_senha_segura
```

Depois force um novo deploy:

- **Manual Deploy** → **Deploy latest commit**

---

## 🔧 Solução 2: Criar via Django Admin Existente

Se você já tiver acesso a um usuário staff (mesmo que não seja superuser):

### Passo 1: Upgrade do Render

O Render oferece **7 dias de trial** do plano pago, que inclui Shell:

1. Dashboard → **Upgrade**
2. Selecione **Starter Plan**
3. Adicione cartão (não será cobrado nos 7 dias)
4. Acesse **Shell**
5. Execute:
   ```bash
   cd biblioteca_online
   python manage.py createsuperuser
   ```
6. Após criar, pode **cancelar** o plano pago e voltar ao Free

---

## 🌐 Solução 3: Interface de Registro + Upgrade Manual

### Passo 1: Criar um usuário comum

1. Acesse: `https://seu-app.onrender.com/registro/`
2. Cadastre um usuário novo
3. Anote o username

### Passo 2: Usar Django Admin Console (Shell Temporário)

**Opção A: Via Railway (tem shell grátis)**

Se quiser, pode fazer o deploy temporariamente no Railway apenas para criar o usuário:

- Railway tem shell grátis
- Após criar o superuser, volte pro Render

**Opção B: Localmente e depois backup**

1. **Localmente**, crie o superusuário:

   ```powershell
   cd biblioteca_online
   python manage.py createsuperuser
   ```

2. **Faça dump dos dados**:

   ```powershell
   python manage.py dumpdata auth.User --indent 2 > users.json
   ```

3. **Suba para produção via fixtures**:
   - Crie um comando que carrega os usuários
   - Ou use ferramenta externa

---

## 🎯 Solução Recomendada

**Use a Solução 1 (Automática)** - Já implementada!

### O que fazer agora:

```powershell
# 1. Commitar
git add .
git commit -m "Adicionar criação automática de superusuário"
git push origin main

# 2. Aguardar deploy (5-10 minutos)

# 3. Acessar o admin
https://seu-app.onrender.com/admin/

# 4. Login com:
Username: admin
Password: admin123456

# 5. IMEDIATAMENTE trocar a senha:
- Clique no seu nome (canto superior direito)
- "Change password"
- Defina uma senha forte
```

---

## 🔒 Trocar Senha Depois

### Via Interface Admin

1. Login no admin: `/admin/`
2. Clique no seu username (canto superior direito)
3. Clique em **"Change password"**
4. Digite a senha atual e a nova senha (2x)
5. Clique em **"Change my password"**

### Criar Outros Superusuários

1. Login no admin como superuser
2. Vá em **Authentication and Authorization** → **Users**
3. Clique em **"Add user"**
4. Preencha username e password
5. Marque:
   - ✅ **Staff status**
   - ✅ **Superuser status**
6. Save

---

## ⚡ Comandos Django Disponíveis

Agora você tem este comando customizado:

```bash
# Criar superuser se não existir
python manage.py create_superuser_if_none
```

---

## 🆘 Troubleshooting

### O superusuário não foi criado

**Verifique os logs do build:**

1. Dashboard → Logs
2. Procure por: `✅ Superusuário "admin" criado com sucesso!`

Se não aparecer, pode ser que já exista. Verifique se consegue fazer login.

### Erro "User already exists"

O comando detecta se já existe superuser e não tenta criar de novo. Isso é normal!

### Não consigo fazer login

Certifique-se de usar:

- Username: `admin` (não é email!)
- Password: `admin123456`

### Quero usar outras credenciais

Adicione no Render (Environment Variables):

```
DJANGO_SUPERUSER_USERNAME=meu_admin
DJANGO_SUPERUSER_EMAIL=meu@email.com
DJANGO_SUPERUSER_PASSWORD=minha_senha_forte_123
```

Force novo deploy: Manual Deploy → Deploy latest commit

---

## 📊 Comparação de Soluções

| Solução             | Tempo  | Dificuldade    | Custo    | Recomendado   |
| ------------------- | ------ | -------------- | -------- | ------------- |
| **1. Automática**   | 5 min  | ⭐ Fácil       | Grátis   | ✅ Sim        |
| **2. Trial 7 dias** | 10 min | ⭐⭐ Médio     | Grátis\* | ⚠️ Temporário |
| **3. Manualmente**  | 30 min | ⭐⭐⭐ Difícil | Grátis   | ❌ Complicado |

\*Requer cartão, mas não cobra nos 7 dias

---

## ✅ Próximos Passos

Após criar o superusuário:

1. [ ] Login no admin
2. [ ] Trocar senha para uma segura
3. [ ] Adicionar alguns livros de exemplo
4. [ ] Criar usuários de teste
5. [ ] Testar todas as funcionalidades

---

**Pronto!** Agora você tem acesso total ao sistema! 🎉

**Lembre-se**: Sempre use senhas fortes em produção! 🔒
