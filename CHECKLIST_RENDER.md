# ✅ Checklist de Deploy no Render

## 📋 Antes de Começar

- [ ] Tenho conta no GitHub
- [ ] Código está no GitHub
- [ ] Li o arquivo DEPLOY_RENDER.md

---

## 🔧 Passo 1: Preparar Localmente (5 minutos)

```powershell
# Commitar tudo
git add .
git commit -m "Preparar para deploy no Render"
git push origin main
```

- [ ] Commitei todos os arquivos
- [ ] Fiz push para o GitHub
- [ ] `.env` NÃO foi commitado (verificar com `git status`)

---

## 🌐 Passo 2: Criar Conta no Render (2 minutos)

1. [ ] Acessei https://render.com
2. [ ] Cliquei em "Get Started for Free"
3. [ ] Fiz login com GitHub
4. [ ] Autorizei o Render

---

## 🗄️ Passo 3: Criar PostgreSQL (3 minutos)

1. [ ] Cliquei em "New +"
2. [ ] Selecionei "PostgreSQL"
3. [ ] Configurei:
   - Name: `biblioteca-db`
   - Database: `biblioteca`
   - User: `biblioteca_user`
   - Plan: **Free**
4. [ ] Cliquei em "Create Database"
5. [ ] Copiei a **Internal Database URL**

📝 Minha Database URL:

```
postgres://biblioteca_user:____@dpg-____.oregon-postgres.render.com/biblioteca
```

---

## 🚀 Passo 4: Criar Web Service (5 minutos)

1. [ ] Cliquei em "New +"
2. [ ] Selecionei "Web Service"
3. [ ] Conectei meu repositório "Biblioteca"
4. [ ] Configurei:
   - Name: `biblioteca-online`
   - Runtime: Python 3
   - Build Command: `bash build.sh`
   - Start Command: `cd biblioteca_online && gunicorn biblioteca_online.wsgi:application`
   - Plan: **Free**

---

## 🔐 Passo 5: Variáveis de Ambiente (3 minutos)

Adicionei estas variáveis (clicando em "Add Environment Variable"):

- [ ] `SECRET_KEY` = `0v9v)y41)waic81^xq=l7rtn#k)(-ef$oub47!!c+re1h%*^f!`
- [ ] `DEBUG` = `False`
- [ ] `DATABASE_URL` = (colei a URL do Passo 3)
- [ ] `DJANGO_SETTINGS_MODULE` = `biblioteca_online.settings_production`
- [ ] `PYTHON_VERSION` = `3.13.0`
- [ ] `ALLOWED_HOSTS` = `.onrender.com`

---

## 🎉 Passo 6: Deploy (10 minutos)

1. [ ] Cliquei em "Create Web Service"
2. [ ] Aguardei o deploy completar
3. [ ] Vi "Build successful!" nos logs
4. [ ] Vi "Server started" nos logs

---

## 👤 Passo 7: Criar Superusuário (2 minutos)

1. [ ] Abri a aba "Shell" no Dashboard
2. [ ] Executei:
   ```bash
   cd biblioteca_online
   python manage.py createsuperuser
   ```
3. [ ] Criei usuário:
   - Username: `_______`
   - Email: `_______`
   - Password: `_______`

---

## 🌍 Passo 8: Testar o Site (5 minutos)

Minha URL: `https://biblioteca-online-____.onrender.com`

Testei:

- [ ] Página inicial abre
- [ ] CSS está funcionando
- [ ] Login do admin funciona (`/admin/`)
- [ ] Posso ver livros
- [ ] Posso cadastrar um livro
- [ ] Posso criar um usuário
- [ ] Empréstimos funcionam
- [ ] Reservas funcionam

---

## 🎯 Finalização

- [ ] Salvei a URL do site
- [ ] Salvei as credenciais do admin
- [ ] Compartilhei o link com alguém
- [ ] Adicionei livros de exemplo

---

## 🆘 Se Algo Der Errado

### Erro no Build?

1. [ ] Verifiquei os logs (Dashboard → Logs)
2. [ ] Procurei erros em vermelho
3. [ ] Consultei DEPLOY_RENDER.md seção "Troubleshooting"

### CSS não carrega?

1. [ ] Verifiquei se `build.sh` executou `collectstatic`
2. [ ] Forcei novo deploy: Manual Deploy → Deploy latest commit

### Erro "DisallowedHost"?

1. [ ] Verifiquei se `ALLOWED_HOSTS=.onrender.com` está nas variáveis

---

## ✅ Deploy Completo!

**Parabéns!** 🎉 Seu sistema está online em:

```
https://biblioteca-online-____.onrender.com
```

### Próximos Passos:

1. [ ] Adicionar mais livros
2. [ ] Testar com amigos
3. [ ] Configurar domínio personalizado (opcional)
4. [ ] Configurar backups do banco
5. [ ] Monitorar logs regularmente

---

**Tempo total estimado: 35 minutos** ⏱️

**Custo: R$ 0,00 (Free Tier)** 💰
