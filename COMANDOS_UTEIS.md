# 📝 Comandos Úteis para Deploy e Manutenção

## 🔍 Verificar antes do Deploy

```bash
# Verificar se está tudo OK
python check_deploy.py

# Verificar erros no Django
cd biblioteca_online
python manage.py check

# Testar localmente com configuração de produção
python manage.py runserver --settings=biblioteca_online.settings_production
```

## 📦 Dependências

```bash
# Instalar dependências
pip install -r requirements.txt

# Atualizar requirements.txt
pip freeze > requirements.txt

# Instalar dependências de produção
pip install gunicorn python-decouple psycopg2-binary whitenoise dj-database-url
```

## 🗄️ Database

```bash
# Fazer migrations
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Backup do banco (SQLite)
cp db.sqlite3 db.sqlite3.backup

# Dump do banco (PostgreSQL)
pg_dump -U usuario -d nome_banco > backup.sql

# Restaurar banco (PostgreSQL)
psql -U usuario -d nome_banco < backup.sql
```

## 📁 Arquivos Estáticos

```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Limpar arquivos estáticos antigos
python manage.py collectstatic --clear --noinput
```

## 🔐 Segurança

```bash
# Gerar SECRET_KEY nova
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Verificar configurações de segurança
python manage.py check --deploy
```

## 🐛 Debug

```bash
# Shell do Django
python manage.py shell

# Shell do Django com IPython
pip install ipython
python manage.py shell

# Ver configurações atuais
python manage.py diffsettings

# Limpar sessões expiradas
python manage.py clearsessions
```

## 🚀 Deploy - Heroku

```bash
# Login
heroku login

# Criar app
heroku create nome-do-app

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Configurar variáveis
heroku config:set SECRET_KEY="sua-chave"
heroku config:set DEBUG=False

# Ver variáveis
heroku config

# Deploy
git push heroku main

# Executar comandos remotamente
heroku run python biblioteca_online/manage.py migrate
heroku run python biblioteca_online/manage.py createsuperuser
heroku run python biblioteca_online/manage.py collectstatic --noinput

# Ver logs
heroku logs --tail

# Reiniciar
heroku restart

# Abrir app
heroku open

# Shell remoto
heroku run bash
```

## 🚂 Deploy - Railway

```bash
# Instalar CLI
npm i -g @railway/cli

# Login
railway login

# Iniciar projeto
railway init

# Link com projeto existente
railway link

# Deploy
railway up

# Ver logs
railway logs

# Adicionar variável
railway variables set SECRET_KEY="sua-chave"

# Executar comando remoto
railway run python biblioteca_online/manage.py migrate

# Shell
railway shell
```

## 🎨 Deploy - Render

```bash
# Ver logs (via dashboard)
# Dashboard → Logs

# Executar comandos (via dashboard)
# Dashboard → Shell

# Build command:
pip install -r requirements.txt

# Start command:
cd biblioteca_online && gunicorn biblioteca_online.wsgi:application --bind 0.0.0.0:$PORT
```

## 🐳 Docker

```bash
# Build imagem
docker build -t biblioteca-online .

# Executar container
docker run -p 8000:8000 biblioteca-online

# Docker Compose
docker-compose up --build

# Parar containers
docker-compose down

# Ver logs
docker-compose logs -f

# Executar comando no container
docker-compose exec web python manage.py migrate
```

## 🔄 Git

```bash
# Commitar mudanças
git add .
git commit -m "Descrição das mudanças"

# Push para GitHub
git push origin main

# Push para Heroku
git push heroku main

# Criar nova branch
git checkout -b nova-feature

# Merge branch
git checkout main
git merge nova-feature

# Ver status
git status

# Ver histórico
git log --oneline
```

## 📊 Monitoramento

```bash
# Ver processos rodando (Heroku)
heroku ps

# Ver uso de recursos (Heroku)
heroku logs --tail | grep "Memory\|CPU"

# Escalar dynos (Heroku)
heroku ps:scale web=1

# Backups (Heroku PostgreSQL)
heroku pg:backups:capture
heroku pg:backups:download
```

## 🧪 Testes

```bash
# Rodar todos os testes
python manage.py test

# Rodar testes de uma app
python manage.py test biblioteca

# Rodar teste específico
python manage.py test biblioteca.tests.test_models

# Com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🧹 Manutenção

```bash
# Limpar arquivos .pyc
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Limpar migrations (CUIDADO!)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recriar migrations
python manage.py makemigrations
python manage.py migrate

# Dump de dados
python manage.py dumpdata > backup.json
python manage.py dumpdata biblioteca > biblioteca_backup.json

# Carregar dados
python manage.py loaddata backup.json
```

## 📈 Performance

```bash
# Profile de queries
pip install django-debug-toolbar

# Ver queries lentas
python manage.py dbshell
EXPLAIN ANALYZE SELECT * FROM biblioteca_livro;

# Cache
python manage.py createcachetable
```

## 🔧 Configuração do Servidor

```bash
# Nginx (configuração básica)
# /etc/nginx/sites-available/biblioteca

server {
    listen 80;
    server_name seu-dominio.com;

    location /static/ {
        alias /caminho/para/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Gunicorn (rodar em produção)
gunicorn biblioteca_online.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
```

## 🆘 Troubleshooting Comum

```bash
# Erro: ModuleNotFoundError
pip install -r requirements.txt

# Erro: DisallowedHost
# Adicione o host em ALLOWED_HOSTS no .env

# Erro: Static files not found
python manage.py collectstatic --noinput

# Erro: Database connection
# Verifique DATABASE_URL no .env

# Limpar cache do Django
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Reset password do admin
python manage.py changepassword nome_usuario
```

---

**Dica:** Salve este arquivo como referência rápida! 📌
