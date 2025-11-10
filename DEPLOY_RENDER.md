# 🎨 Guia Completo de Deploy no Render

## ✅ Pré-requisitos

- [x] Conta no GitHub
- [x] Código commitado e no GitHub
- [x] Arquivos de deploy criados (build.sh, render.yaml)

---

## 📝 Passo 1: Commitar e Enviar para o GitHub

```powershell
# Verificar status
git status

# Adicionar todos os arquivos
git add .

# Commitar
git commit -m "Preparar para deploy no Render"

# Enviar para o GitHub
git push origin main
```

⚠️ **IMPORTANTE**: Verifique se o `.env` NÃO foi commitado (já está no .gitignore)

---

## 🌐 Passo 2: Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. **Sign up with GitHub** (recomendado)
4. Autorize o Render a acessar seus repositórios

---

## 🗄️ Passo 3: Criar Banco de Dados PostgreSQL

### 3.1 Criar o Banco

1. No Dashboard do Render, clique em **"New +"**
2. Selecione **"PostgreSQL"**
3. Configure:
   - **Name**: `biblioteca-db`
   - **Database**: `biblioteca`
   - **User**: `biblioteca_user`
   - **Region**: Escolha a mais próxima (ex: Oregon USA)
   - **PostgreSQL Version**: 16 (mais recente)
   - **Plan**: **Free** (perfeito para começar)

4. Clique em **"Create Database"**

### 3.2 Copiar a Database URL

Após criar o banco, você verá várias informações. Copie:

- **Internal Database URL** (começa com `postgres://...`)

📋 Exemplo: `postgres://biblioteca_user:senha123@dpg-xxxxx.oregon-postgres.render.com/biblioteca`

⚠️ **GUARDE ESTA URL** - você vai precisar dela no próximo passo!

---

## 🚀 Passo 4: Criar Web Service

### 4.1 Novo Web Service

1. No Dashboard, clique em **"New +"**
2. Selecione **"Web Service"**
3. Clique em **"Build and deploy from a Git repository"**
4. Clique em **"Next"**

### 4.2 Conectar Repositório

1. Se for a primeira vez:
   - Clique em **"Connect account"** (GitHub)
   - Autorize o Render
   
2. Encontre seu repositório **"Biblioteca"**
3. Clique em **"Connect"**

### 4.3 Configurar o Web Service

Preencha os campos:

| Campo | Valor |
|-------|-------|
| **Name** | `biblioteca-online` (ou seu nome preferido) |
| **Region** | Same as database (mesma do banco) |
| **Branch** | `main` |
| **Root Directory** | (deixe vazio) |
| **Runtime** | `Python 3` |
| **Build Command** | `bash build.sh` |
| **Start Command** | `cd biblioteca_online && gunicorn biblioteca_online.wsgi:application` |
| **Plan** | **Free** |

---

## 🔐 Passo 5: Configurar Variáveis de Ambiente

### 5.1 Adicionar Variáveis

Na seção **"Environment Variables"**, clique em **"Add Environment Variable"** e adicione:

#### Variável 1: SECRET_KEY
```
Key: SECRET_KEY
Value: 0v9v)y41)waic81^xq=l7rtn#k)(-ef$oub47!!c+re1h%*^f!
```
(ou gere uma nova em: https://djecrety.ir/)

#### Variável 2: DEBUG
```
Key: DEBUG
Value: False
```

#### Variável 3: DATABASE_URL
```
Key: DATABASE_URL
Value: [Cole a Internal Database URL do Passo 3.2]
```

#### Variável 4: DJANGO_SETTINGS_MODULE
```
Key: DJANGO_SETTINGS_MODULE
Value: biblioteca_online.settings_production
```

#### Variável 5: PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.13.0
```

#### Variável 6: ALLOWED_HOSTS
```
Key: ALLOWED_HOSTS
Value: .onrender.com
```

### 5.2 Exemplo Completo

```
SECRET_KEY=0v9v)y41)waic81^xq=l7rtn#k)(-ef$oub47!!c+re1h%*^f!
DEBUG=False
DATABASE_URL=postgres://biblioteca_user:xxxxx@dpg-xxxxx.oregon-postgres.render.com/biblioteca
DJANGO_SETTINGS_MODULE=biblioteca_online.settings_production
PYTHON_VERSION=3.13.0
ALLOWED_HOSTS=.onrender.com
```

---

## 🎉 Passo 6: Criar o Web Service

1. Revise todas as configurações
2. Clique em **"Create Web Service"**
3. Aguarde o deploy (5-10 minutos na primeira vez)

### Acompanhe o Deploy

Você verá logs em tempo real:
```
==> Installing dependencies...
==> Collecting static files...
==> Running migrations...
==> Build successful!
==> Starting server...
```

---

## 👤 Passo 7: Criar Superusuário

### 7.1 Acessar Shell

1. No Dashboard do seu Web Service
2. Clique na aba **"Shell"**
3. Aguarde o shell carregar

### 7.2 Criar Superusuário

Execute no shell:
```bash
cd biblioteca_online
python manage.py createsuperuser
```

Preencha:
- **Username**: admin (ou seu nome)
- **Email**: seu@email.com
- **Password**: (digite uma senha forte)
- **Password (again)**: (repita a senha)

---

## 🌍 Passo 8: Acessar Seu Site

### 8.1 Obter URL

No topo do Dashboard você verá:
```
https://biblioteca-online-xxxx.onrender.com
```

### 8.2 Testar

1. **Página inicial**: `https://seu-app.onrender.com/`
2. **Admin**: `https://seu-app.onrender.com/admin/`
3. **Registro**: `https://seu-app.onrender.com/registro/`

---

## ✅ Checklist Final

Antes de considerar o deploy completo, verifique:

- [ ] Site abre sem erros
- [ ] Login do admin funciona
- [ ] Página de livros carrega
- [ ] CSS está funcionando
- [ ] Pode criar um livro novo
- [ ] Pode criar um usuário novo
- [ ] Empréstimos funcionam
- [ ] Reservas funcionam

---

## 🔧 Configurações Adicionais

### Domínio Personalizado

1. No Dashboard → **Settings**
2. Seção **"Custom Domain"**
3. Clique em **"Add Custom Domain"**
4. Siga as instruções para configurar DNS

### SSL/HTTPS

✅ O Render configura HTTPS automaticamente! Seu site já está seguro.

### Auto-Deploy

✅ Já está ativado! Toda vez que você fizer `git push`, o Render faz deploy automaticamente.

---

## 🐛 Troubleshooting

### Erro: "Application failed to respond"

**Causa**: Build falhou ou servidor não iniciou

**Solução**:
1. Verifique os logs no Dashboard
2. Procure por erros em vermelho
3. Verifique se `DATABASE_URL` está correto
4. Verifique se `build.sh` tem permissão de execução

### Erro: "DisallowedHost"

**Causa**: ALLOWED_HOSTS não configurado

**Solução**:
Adicione variável de ambiente:
```
ALLOWED_HOSTS=.onrender.com
```

### CSS não carrega

**Causa**: Arquivos estáticos não foram coletados

**Solução**:
1. Verifique se `build.sh` está executando `collectstatic`
2. Force um novo deploy: **Manual Deploy** → **Deploy latest commit**

### Banco de dados vazio

**Causa**: Migrations não foram executadas

**Solução**:
No Shell:
```bash
cd biblioteca_online
python manage.py migrate
```

### "Internal Server Error"

**Causa**: Múltiplas possibilidades

**Solução**:
1. Verifique logs: Dashboard → **Logs**
2. Procure por traceback em Python
3. Verifique se todas as variáveis de ambiente estão corretas

---

## 🔄 Atualizações

### Como atualizar o site após mudanças

```powershell
# 1. Fazer mudanças no código
# 2. Commitar
git add .
git commit -m "Descrição das mudanças"

# 3. Push para GitHub
git push origin main

# 4. Render faz deploy automaticamente! 🎉
```

### Deploy Manual

Se quiser forçar um deploy:
1. Dashboard → **Manual Deploy**
2. Clique em **"Deploy latest commit"**

---

## 📊 Monitoramento

### Ver Logs

Dashboard → **Logs**
- Logs em tempo real
- Erros aparecem em vermelho
- Pode filtrar por tipo

### Ver Métricas

Dashboard → **Metrics**
- CPU usage
- Memory usage
- Request rate
- Response time

### Reiniciar Serviço

Dashboard → **Manual Deploy** → **"Clear build cache & deploy"**

---

## 💰 Plano Free vs Paid

### Plano Free (Grátis)
- ✅ 750 horas/mês
- ✅ SSL grátis
- ✅ Deploy automático
- ⚠️ Inativo após 15 min sem requisições
- ⚠️ 100GB de largura de banda

### Plano Starter ($7/mês)
- ✅ Sempre ativo
- ✅ Mais recursos (RAM, CPU)
- ✅ Largura de banda ilimitada

**Para começar, o Free é perfeito!** 🎉

---

## 🆘 Precisa de Ajuda?

- **Documentação Oficial**: https://render.com/docs
- **Suporte**: https://render.com/support
- **Status**: https://status.render.com

---

## 🎯 Próximos Passos

Após o deploy bem-sucedido:

1. ✅ Adicione alguns livros de exemplo
2. ✅ Teste todas as funcionalidades
3. ✅ Compartilhe o link com amigos
4. ✅ Configure backup do banco de dados
5. ✅ Considere domínio personalizado

---

**Parabéns pelo deploy! 🚀📚**

Seu sistema de biblioteca está online e acessível para o mundo!
