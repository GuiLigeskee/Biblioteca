"""
Comando para criar superusuário automaticamente
Útil para deploy em plataformas sem acesso a shell
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria um superusuário automaticamente se não existir'

    def handle(self, *args, **options):
        # Verificar se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superusuário já existe. Nenhuma ação necessária.')
            )
            return

        # Credenciais padrão (você pode mudar depois via admin)
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@biblioteca.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')

        # Criar superusuário
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f'✅ Superusuário "{username}" criado com sucesso!')
        )
        self.stdout.write(
            self.style.WARNING(f'⚠️  Username: {username}')
        )
        self.stdout.write(
            self.style.WARNING(f'⚠️  Password: {password}')
        )
        self.stdout.write(
            self.style.WARNING('⚠️  IMPORTANTE: Troque a senha após o primeiro login!')
        )
