from django.shortcuts import render, get_object_or_404, redirect
from .models import Livro, Emprestimo, Reserva
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages


def lista_livros(request):
    busca = request.GET.get('busca', '')
    if busca:
        livros = Livro.objects.filter(titulo__icontains=busca)
    else:
        livros = Livro.objects.all()
    return render(request, 'biblioteca/lista_livros.html', {'livros': livros})

def detalhes_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'biblioteca/detalhes_livro.html', {'livro': livro})


@login_required
def solicitar_emprestimo(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if livro.disponivel:
        data_devolucao = timezone.now() + timedelta(days=7)
        
        emprestimo = Emprestimo(usuario=request.user, livro=livro, data_devolucao=data_devolucao)
        emprestimo.save()

        livro.disponivel = False
        livro.save()

        messages.success(request, "Empréstimo realizado com sucesso!")
    else:
        messages.error(request, "Este livro não está disponível para empréstimo no momento.")

    return redirect('detalhes_livro', pk=livro.pk)

@login_required
def meus_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(usuario=request.user, devolvido=False)
    return render(request, 'biblioteca/meus_emprestimos.html', {'emprestimos': emprestimos})

from django.contrib import messages


@login_required
def criar_reserva(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if not livro.disponivel:
        # Cria a reserva
        reserva = Reserva(usuario=request.user, livro=livro)
        reserva.save()
        
        messages.success(request, "Reserva realizada com sucesso!")
    else:
        messages.error(request, "Este livro está disponível para empréstimo, não é necessário reservar.")

    return redirect('detalhes_livro', pk=livro.pk)



@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    reservas_atualizadas = []

    for reserva in reservas:
        if reserva.livro.disponivel and not reserva.notificado:
            reserva.notificado = True
            reserva.save()
        reservas_atualizadas.append({
            'livro': reserva.livro,
            'data_reserva': reserva.data_reserva,
            'disponivel': reserva.livro.disponivel,
            'notificado': reserva.notificado
        })

    return render(request, 'biblioteca/minhas_reservas.html', {'reservas': reservas_atualizadas})


@login_required
def marcar_como_devolvido(request, pk):
    if not request.user.is_staff:
        return redirect('lista_livros')

    emprestimo = get_object_or_404(Emprestimo, livro__pk=pk, devolvido=False)

    emprestimo.devolvido = True
    emprestimo.save()

    livro = emprestimo.livro
    livro.disponivel = True
    livro.save()

    return redirect('detalhes_livro', pk=pk)

def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    if request.user == emprestimo.usuario:
        if not emprestimo.devolvido:
            emprestimo.devolvido = True
            emprestimo.save()

            multa = emprestimo.calcular_multa()

            usuario = request.user
            usuario.multa += multa 
            usuario.save()

            return redirect('meus_emprestimos')
        else:
            return HttpResponse("O livro já foi devolvido.", status=400)
    return HttpResponse("Você não tem permissão para devolver este livro.", status=403)



def detalhes_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    emprestado = Emprestimo.objects.filter(livro=livro, devolvido=False).exists()
    
    return render(request, 'biblioteca/detalhes_livro.html', {'livro': livro, 'emprestado': emprestado})

