from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)
    data_publicacao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

# models.py
class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    notificado = models.BooleanField(default=False)  # Indica se o usuário foi notificado



class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField()
    devolvido = models.BooleanField(default=False)

    def dias_atraso(self):
        if self.devolvido:
            return 0
        hoje = date.today()
        return (hoje - self.data_devolucao).days if hoje > self.data_devolucao else 0

    def calcular_multa(self):
        atraso = self.dias_atraso()
        return atraso * 1 

