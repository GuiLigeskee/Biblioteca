from django.contrib import admin
from .models import Livro, Emprestimo, Reserva, PerfilUsuario, Admin

class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['livro', 'usuario', 'data_emprestimo', 'data_devolucao_prevista', 'data_devolucao_real', 'multa']
    list_filter = ['data_emprestimo']
    actions = ['marcar_como_devolvido']

    def marcar_como_devolvido(self, request, queryset):
        from django.utils import timezone
        for emprestimo in queryset:
            if not emprestimo.data_devolucao_real:
                emprestimo.data_devolucao_real = timezone.now()
                emprestimo.calcular_multa()
                emprestimo.save()
        self.message_user(request, "Livros selecionados marcados como devolvidos.")
    marcar_como_devolvido.short_description = "Marcar livros selecionados como devolvidos"

class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'editora', 'ano_publicacao', 'isbn', 'quantidade_total', 'quantidade_disponivel']
    search_fields = ['titulo', 'autor', 'isbn']
    list_filter = ['genero', 'ano_publicacao']

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'livro', 'data_reserva', 'status']
    list_filter = ['status', 'data_reserva']

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpf', 'telefone', 'data_nascimento']
    search_fields = ['user__username', 'cpf']

class AdminModelAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'nivel_acesso']
    list_filter = ['nivel_acesso']

admin.site.register(Livro, LivroAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Admin, AdminModelAdmin)

