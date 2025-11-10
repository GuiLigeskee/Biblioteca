# 🚀 Deploy Rápido - 3 Passos

## Opção Mais Simples: Railway (Recomendado para iniciantes)

### 1️⃣ Preparar o projeto (10 minutos)

```bash
# 1. Criar arquivo .env
cp .env.example .env

# 2. Editar .env com sua SECRET_KEY
# Gere uma chave em: https://djecrety.ir/

# 3. Commitar tudo
git add .
git commit -m "Preparar para deploy"
git push origin main
```

### 2️⃣ Criar conta no Railway (5 minutos)

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Login com GitHub
4. Autorize o Railway

### 3️⃣ Deploy (5 minutos)

1. **New Project** → **Deploy from GitHub repo**
2. Selecione seu repositório `Biblioteca`
3. **Add variables:**
   - `SECRET_KEY`: (sua chave gerada)
   - `DEBUG`: `False`
   - `DJANGO_SETTINGS_MODULE`: `biblioteca_online.settings_production`
4. **Add Database:**
   - New → Database → PostgreSQL
   - Railway conecta automaticamente
5. Aguarde o deploy (2-3 minutos)
6. **Generate Domain** para ter uma URL pública

### 4️⃣ Configurações finais

```bash
# Executar migrations no Railway Terminal
railway run python biblioteca_online/manage.py migrate

# Criar superusuário
railway run python biblioteca_online/manage.py createsuperuser

# Coletar arquivos estáticos
railway run python biblioteca_online/manage.py collectstatic --noinput
```

## ✅ Pronto!

Acesse sua URL e teste: `https://seu-projeto.railway.app`

---

## Alternativas Rápidas

### Render (Grátis com limitações)

1. https://render.com → New → Web Service
2. Conecte GitHub
3. Configure variáveis de ambiente
4. Deploy automático!

### Heroku (Pago, mais robusto)

```bash
heroku create biblioteca-online
heroku addons:create heroku-postgresql
git push heroku main
heroku run python biblioteca_online/manage.py migrate
```

---

## 🆘 Problemas?

Execute o verificador:

```bash
python check_deploy.py
```

Leia o guia completo: **DEPLOY.md**

---

**Dica:** Railway oferece $5 de crédito grátis por mês! Perfeito para projetos pequenos. 🎉
