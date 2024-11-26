from django.core.management.base import BaseCommand
from biblioteca.models import Reserva

class Command(BaseCommand):
    help = 'Verifica livros disponíveis e atualiza reservas'

    def handle(self, *args, **kwargs):
        reservas = Reserva.objects.filter(livro__disponivel=True, notificado=False)
        for reserva in reservas:
            reserva.notificado = True
            reserva.save()
            self.stdout.write(f"Reserva do livro '{reserva.livro.titulo}' atualizada.")
