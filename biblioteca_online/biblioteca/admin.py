from django.contrib import admin
from .models import Livro, Emprestimo, Reserva

class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['livro', 'usuario', 'data_emprestimo', 'data_devolucao', 'devolvido']
    list_filter = ['devolvido']
    actions = ['marcar_como_devolvido']

    def marcar_como_devolvido(self, request, queryset):
        for emprestimo in queryset:
            if not emprestimo.devolvido:
                emprestimo.devolvido = True
                emprestimo.save()
        self.message_user(request, "Livros selecionados marcados como devolvidos.")
    marcar_como_devolvido.short_description = "Marcar livros selecionados como devolvidos"

admin.site.register(Livro)
admin.site.register(Emprestimo, EmprestimoAdmin)
admin.site.register(Reserva)
