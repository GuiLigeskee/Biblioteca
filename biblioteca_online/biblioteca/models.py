from django.db import models
from django.contrib.auth.models import User
from datetime import date

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)  # Formato XXX.XXX.XXX-XX
    data_nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    editora = models.CharField(max_length=200, blank=True, null=True)
    ano_publicacao = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    quantidade_total = models.IntegerField(default=1)
    quantidade_disponivel = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

# models.py
class Reserva(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"



class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao_prevista = models.DateTimeField(null=True, blank=True)
    data_devolucao_real = models.DateTimeField(null=True, blank=True)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def dias_atraso(self):
        if self.data_devolucao_real or not self.data_devolucao_prevista:
            return 0
        hoje = date.today()
        data_prevista = self.data_devolucao_prevista.date()
        return (hoje - data_prevista).days if hoje > data_prevista else 0

    def calcular_multa(self):
        atraso = self.dias_atraso()
        self.multa = atraso * 1.00  # R$ 1,00 por dia de atraso
        return self.multa
    
    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"


class Admin(models.Model):
    NIVEL_ACESSO_CHOICES = [
        (1, 'Geral'),
        (2, 'Superadmin'),
    ]
    
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    senha = models.CharField(max_length=128)  # Usar hash em produção
    nivel_acesso = models.IntegerField(choices=NIVEL_ACESSO_CHOICES, default=1)

    def __str__(self):
        return f"{self.nome} - Nível {self.nivel_acesso}"
