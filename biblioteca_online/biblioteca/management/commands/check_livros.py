"""
Script para verificar e atualizar dados dos livros
"""
from django.core.management.base import BaseCommand
from biblioteca.models import Livro

class Command(BaseCommand):
    help = 'Verifica e exibe informações dos livros cadastrados'

    def handle(self, *args, **options):
        livros = Livro.objects.all()
        
        if not livros.exists():
            self.stdout.write(
                self.style.WARNING('Nenhum livro cadastrado no sistema.')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'\n📚 Total de livros: {livros.count()}\n')
        )

        for livro in livros:
            self.stdout.write(f'\n{"="*60}')
            self.stdout.write(f'ID: {livro.id}')
            self.stdout.write(f'Título: {livro.titulo}')
            self.stdout.write(f'Autor: {livro.autor}')
            self.stdout.write(f'Editora: {livro.editora if livro.editora else "⚠️  NÃO INFORMADO"}')
            self.stdout.write(f'Ano: {livro.ano_publicacao if livro.ano_publicacao else "⚠️  NÃO INFORMADO"}')
            self.stdout.write(f'Gênero: {livro.genero}')
            self.stdout.write(f'ISBN: {livro.isbn if livro.isbn else "⚠️  NÃO INFORMADO"}')
            self.stdout.write(f'Qtd Total: {livro.quantidade_total}')
            self.stdout.write(f'Qtd Disponível: {livro.quantidade_disponivel}')
            
        self.stdout.write(f'\n{"="*60}\n')
        
        # Contar livros sem editora ou ano
        sem_editora = livros.filter(editora__isnull=True).count() + livros.filter(editora='').count()
        sem_ano = livros.filter(ano_publicacao__isnull=True).count()
        
        if sem_editora > 0:
            self.stdout.write(
                self.style.WARNING(f'⚠️  {sem_editora} livro(s) sem editora informada')
            )
        
        if sem_ano > 0:
            self.stdout.write(
                self.style.WARNING(f'⚠️  {sem_ano} livro(s) sem ano de publicação informado')
            )
        
        if sem_editora == 0 and sem_ano == 0:
            self.stdout.write(
                self.style.SUCCESS('✅ Todos os livros têm editora e ano informados!')
            )
