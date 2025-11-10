# 🚀 Guia de Deploy - Biblioteca Online

Este guia mostra como fazer deploy da aplicação em diferentes plataformas.

## 📋 Pré-requisitos

1. Git instalado e configurado
2. Conta na plataforma escolhida (Heroku, Railway, Render, etc.)
3. Código commitado no Git

## 🔧 Preparação do Projeto

### 1. Criar arquivo .env

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=.herokuapp.com,.railway.app,seu-dominio.com
DATABASE_URL=postgres://usuario:senha@host:5432/database
```

### 2. Instalar dependências de produção

```bash
pip install -r requirements.txt
```

### 3. Coletar arquivos estáticos

```bash
cd biblioteca_online
python manage.py collectstatic --noinput
```

### 4. Fazer migrations

```bash
python manage.py migrate
```

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

---

## 🎯 Opção 1: Deploy no Heroku (Recomendado)

### Passo 1: Instalar Heroku CLI

Baixe em: https://devcenter.heroku.com/articles/heroku-cli

### Passo 2: Fazer login

```bash
heroku login
```

### Passo 3: Criar aplicação

```bash
heroku create nome-da-sua-biblioteca
```

### Passo 4: Adicionar PostgreSQL

```bash
heroku addons:create heroku-postgresql:essential-0
```

### Passo 5: Configurar variáveis de ambiente

```bash
heroku config:set SECRET_KEY="sua-chave-secreta-super-segura"
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=biblioteca_online.settings_production
```

### Passo 6: Deploy

```bash
git add .
git commit -m "Preparar para deploy"
git push heroku main
```

### Passo 7: Executar migrations

```bash
heroku run python biblioteca_online/manage.py migrate
heroku run python biblioteca_online/manage.py createsuperuser
```

### Passo 8: Abrir aplicação

```bash
heroku open
```

### Comandos úteis Heroku:

```bash
# Ver logs
heroku logs --tail

# Executar shell
heroku run python biblioteca_online/manage.py shell

# Reiniciar aplicação
heroku restart

# Ver configurações
heroku config
```

---

## 🚂 Opção 2: Deploy no Railway

### Passo 1: Criar conta

Acesse: https://railway.app

### Passo 2: Novo projeto

1. Clique em "New Project"
2. Selecione "Deploy from GitHub repo"
3. Conecte seu repositório

### Passo 3: Adicionar PostgreSQL

1. Clique em "New"
2. Selecione "Database" → "PostgreSQL"

### Passo 4: Configurar variáveis

Na aba "Variables", adicione:

```
SECRET_KEY=sua-chave-secreta
DEBUG=False
DJANGO_SETTINGS_MODULE=biblioteca_online.settings_production
```

Railway vai pegar a DATABASE_URL automaticamente do PostgreSQL.

### Passo 5: Deploy automático

Railway faz deploy automaticamente a cada push no GitHub!

---

## 🎨 Opção 3: Deploy no Render

### Passo 1: Criar conta

Acesse: https://render.com

### Passo 2: Novo Web Service

1. New → Web Service
2. Conecte seu repositório GitHub
3. Configure:
   - **Name:** biblioteca-online
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd biblioteca_online && gunicorn biblioteca_online.wsgi`

### Passo 3: Adicionar PostgreSQL

1. New → PostgreSQL
2. Nomeie o banco
3. Copie a "Internal Database URL"

### Passo 4: Variáveis de ambiente

Em "Environment", adicione:

```
SECRET_KEY=sua-chave-secreta
DEBUG=False
DATABASE_URL=(cole a URL do PostgreSQL)
DJANGO_SETTINGS_MODULE=biblioteca_online.settings_production
```

### Passo 5: Deploy

Clique em "Create Web Service" e aguarde!

---

## 🐳 Opção 4: Deploy com Docker

### Criar Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/biblioteca_online

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "biblioteca_online.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Criar docker-compose.yml

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: biblioteca
      POSTGRES_USER: bibliotecauser
      POSTGRES_PASSWORD: senha_segura

  web:
    build: .
    command: gunicorn biblioteca_online.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
```

### Executar

```bash
docker-compose up --build
```

---

## 🔒 Checklist de Segurança

Antes de fazer deploy, certifique-se de:

- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` única e segura (não use a do repositório!)
- [ ] `.env` está no `.gitignore`
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] PostgreSQL configurado (não use SQLite em produção)
- [ ] Arquivos estáticos coletados
- [ ] HTTPS ativado (SSL)
- [ ] Backups do banco de dados configurados

---

## 🐛 Troubleshooting

### Erro: "Application Error"

```bash
# Veja os logs
heroku logs --tail  # ou Railway/Render dashboard
```

### Erro: "DisallowedHost"

Adicione seu domínio em `ALLOWED_HOSTS` no `.env`

### Erro: "Static files not found"

```bash
python manage.py collectstatic --noinput
```

### Erro: "Database connection failed"

Verifique se `DATABASE_URL` está correta no `.env`

### Site carrega mas sem CSS

Verifique:

1. `STATIC_ROOT` configurado
2. `collectstatic` executado
3. WhiteNoise instalado

---

## 📊 Monitoramento

### Ver logs em tempo real

```bash
# Heroku
heroku logs --tail

# Railway
Acesse Dashboard → Deployments → View Logs

# Render
Acesse Dashboard → Logs
```

### Executar comandos remotamente

```bash
# Heroku
heroku run python biblioteca_online/manage.py shell

# Railway/Render
Use o shell do dashboard
```

---

## 🔄 Atualizações

Para atualizar o site após mudanças no código:

```bash
git add .
git commit -m "Descrição das mudanças"
git push heroku main  # ou git push origin main para Railway/Render
```

Railway e Render fazem deploy automático!

---

## 💰 Custos Estimados

| Plataforma         | Gratuito          | Pago      |
| ------------------ | ----------------- | --------- |
| **Heroku**         | ❌ Não mais       | $7-25/mês |
| **Railway**        | $5 crédito/mês    | $5-20/mês |
| **Render**         | ✅ Sim (limitado) | $7-25/mês |
| **PythonAnywhere** | ✅ Sim (limitado) | $5-50/mês |

---

## 📞 Próximos Passos

Após o deploy:

1. ✅ Acesse `/admin/` e faça login
2. ✅ Crie alguns livros de exemplo
3. ✅ Teste o cadastro de usuários
4. ✅ Teste empréstimos e reservas
5. ✅ Configure backup automático do banco
6. ✅ Configure domínio personalizado (opcional)

---

## 🆘 Precisa de Ajuda?

- **Documentação Django Deploy:** https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Heroku Python:** https://devcenter.heroku.com/articles/getting-started-with-python
- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs

---

Boa sorte com seu deploy! 🚀📚
