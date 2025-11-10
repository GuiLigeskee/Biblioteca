from django.shortcuts import render, get_object_or_404, redirect
from .models import Livro, Emprestimo, Reserva, PerfilUsuario
from .forms import RegistroUsuarioForm, LivroForm, EmprestimoForm, ReservaForm, PerfilUsuarioForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login


# ========== VIEWS PÚBLICAS ==========

def lista_livros(request):
    busca = request.GET.get('busca', '')
    genero = request.GET.get('genero', '')
    
    livros = Livro.objects.all()
    
    if busca:
        livros = livros.filter(titulo__icontains=busca) | livros.filter(autor__icontains=busca)
    
    if genero:
        livros = livros.filter(genero__icontains=genero)
    
    generos = Livro.objects.values_list('genero', flat=True).distinct()
    
    return render(request, 'biblioteca/lista_livros.html', {
        'livros': livros, 
        'generos': generos,
        'busca': busca,
        'genero_selecionado': genero
    })


def detalhes_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    tem_estoque = livro.quantidade_disponivel > 0
    usuario_tem_reserva = False
    
    if request.user.is_authenticated:
        usuario_tem_reserva = Reserva.objects.filter(
            livro=livro, 
            usuario=request.user, 
            status='ativa'
        ).exists()
    
    return render(request, 'biblioteca/detalhes_livro.html', {
        'livro': livro, 
        'tem_estoque': tem_estoque,
        'usuario_tem_reserva': usuario_tem_reserva
    })


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('lista_livros')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'biblioteca/registro_usuario.html', {'form': form})


# ========== VIEWS DE EMPRÉSTIMOS ==========

@login_required
def solicitar_emprestimo(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if livro.quantidade_disponivel > 0:
        data_devolucao_prevista = timezone.now() + timedelta(days=7)
        
        emprestimo = Emprestimo(
            usuario=request.user, 
            livro=livro, 
            data_devolucao_prevista=data_devolucao_prevista
        )
        emprestimo.save()

        livro.quantidade_disponivel -= 1
        livro.save()

        messages.success(request, f"Empréstimo realizado com sucesso! Devolução prevista: {data_devolucao_prevista.strftime('%d/%m/%Y')}")
    else:
        messages.error(request, "Este livro não está disponível para empréstimo no momento.")

    return redirect('detalhes_livro', pk=livro.pk)


@login_required
def meus_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(
        usuario=request.user, 
        data_devolucao_real__isnull=True
    ).order_by('-data_emprestimo')
    
    # Calcular multas para cada empréstimo
    for emprestimo in emprestimos:
        emprestimo.dias_em_atraso = emprestimo.dias_atraso()
        emprestimo.valor_multa = emprestimo.calcular_multa()
    
    return render(request, 'biblioteca/meus_emprestimos.html', {'emprestimos': emprestimos})


@login_required
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    
    if request.user != emprestimo.usuario:
        messages.error(request, "Você não tem permissão para devolver este livro.")
        return redirect('meus_emprestimos')
    
    if emprestimo.data_devolucao_real:
        messages.warning(request, "O livro já foi devolvido.")
        return redirect('meus_emprestimos')
    
    # Registrar devolução
    emprestimo.data_devolucao_real = timezone.now()
    emprestimo.calcular_multa()
    emprestimo.save()
    
    # Aumentar quantidade disponível
    livro = emprestimo.livro
    livro.quantidade_disponivel += 1
    livro.save()
    
    if emprestimo.multa > 0:
        messages.warning(request, f"Livro devolvido! Você tem uma multa de R$ {emprestimo.multa:.2f} por atraso de {emprestimo.dias_atraso()} dia(s).")
    else:
        messages.success(request, "Livro devolvido com sucesso!")
    
    return redirect('meus_emprestimos')


# ========== VIEWS DE RESERVAS ==========

@login_required
def criar_reserva(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    # Verificar se já tem reserva ativa
    reserva_existente = Reserva.objects.filter(
        usuario=request.user, 
        livro=livro, 
        status='ativa'
    ).exists()
    
    if reserva_existente:
        messages.warning(request, "Você já tem uma reserva ativa para este livro.")
        return redirect('detalhes_livro', pk=livro.pk)

    if livro.quantidade_disponivel == 0:
        # Cria a reserva
        reserva = Reserva(usuario=request.user, livro=livro, status='ativa')
        reserva.save()
        
        messages.success(request, "Reserva realizada com sucesso! Você será notificado quando o livro estiver disponível.")
    else:
        messages.info(request, "Este livro está disponível para empréstimo. Não é necessário fazer reserva.")

    return redirect('detalhes_livro', pk=livro.pk)


@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_reserva')
    
    reservas_info = []
    for reserva in reservas:
        info = {
            'id': reserva.id,
            'livro': reserva.livro,
            'data_reserva': reserva.data_reserva,
            'status': reserva.status,
            'disponivel': reserva.livro.quantidade_disponivel > 0
        }
        reservas_info.append(info)

    return render(request, 'biblioteca/minhas_reservas.html', {'reservas': reservas_info})


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    if reserva.status == 'ativa':
        reserva.status = 'cancelada'
        reserva.save()
        messages.success(request, "Reserva cancelada com sucesso!")
    else:
        messages.warning(request, "Esta reserva não pode ser cancelada.")
    
    return redirect('minhas_reservas')


# ========== VIEWS DE PERFIL ==========

@login_required
def editar_perfil(request):
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = PerfilUsuario(user=request.user)
        perfil.save()
    
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil, user=request.user)
        if form.is_valid():
            # Atualizar dados do User
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            # Atualizar perfil
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('editar_perfil')
    else:
        form = PerfilUsuarioForm(instance=perfil, user=request.user)
    
    return render(request, 'biblioteca/editar_perfil.html', {'form': form})


# ========== VIEWS ADMINISTRATIVAS ==========

@staff_member_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect('lista_livros')
    else:
        form = LivroForm()
    
    return render(request, 'biblioteca/cadastrar_livro.html', {'form': form})


@staff_member_required
def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect('detalhes_livro', pk=livro.pk)
    else:
        form = LivroForm(instance=livro)
    
    return render(request, 'biblioteca/editar_livro.html', {'form': form, 'livro': livro})


@staff_member_required
def criar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empréstimo criado com sucesso!")
            return redirect('lista_emprestimos')
    else:
        form = EmprestimoForm()
    
    return render(request, 'biblioteca/criar_emprestimo.html', {'form': form})


@staff_member_required
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    
    # Adicionar informações de multa
    for emprestimo in emprestimos:
        emprestimo.dias_em_atraso = emprestimo.dias_atraso()
        emprestimo.valor_multa = emprestimo.calcular_multa()
    
    return render(request, 'biblioteca/lista_emprestimos.html', {'emprestimos': emprestimos})


@staff_member_required
def lista_reservas(request):
    reservas = Reserva.objects.all().order_by('-data_reserva')
    return render(request, 'biblioteca/lista_reservas.html', {'reservas': reservas})


@staff_member_required
def marcar_como_devolvido(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    
    if not emprestimo.data_devolucao_real:
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.calcular_multa()
        emprestimo.save()
        
        # Aumentar quantidade disponível
        livro = emprestimo.livro
        livro.quantidade_disponivel += 1
        livro.save()
        
        messages.success(request, "Empréstimo marcado como devolvido!")
    else:
        messages.warning(request, "Este empréstimo já foi devolvido.")
    
    return redirect('lista_emprestimos')
