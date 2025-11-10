#!/usr/bin/env bash
# Script de build para o Render

set -o errexit

# Instalar dependências
pip install -r requirements.txt

# Coletar arquivos estáticos
cd biblioteca_online
python manage.py collectstatic --no-input

# Executar migrations
python manage.py migrate
