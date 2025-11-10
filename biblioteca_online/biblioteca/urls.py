from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Páginas públicas
    path('', views.lista_livros, name='lista_livros'),
    path('livros/<int:pk>/', views.detalhes_livro, name='detalhes_livro'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='biblioteca/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='lista_livros'), name='logout'),
    
    # Empréstimos (usuário)
    path('livros/<int:pk>/emprestar/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('meus-emprestimos/', views.meus_emprestimos, name='meus_emprestimos'),
    path('emprestimos/<int:emprestimo_id>/devolver/', views.devolver_livro, name='devolver_livro'),
    
    # Reservas (usuário)
    path('livros/<int:pk>/reservar/', views.criar_reserva, name='criar_reserva'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('reservas/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    
    # Perfil
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    
    # Administração - Livros
    path('admin/livros/cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('admin/livros/<int:pk>/editar/', views.editar_livro, name='editar_livro'),
    
    # Administração - Empréstimos
    path('admin/emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('admin/emprestimos/criar/', views.criar_emprestimo, name='criar_emprestimo'),
    path('admin/emprestimos/<int:pk>/devolver/', views.marcar_como_devolvido, name='marcar_como_devolvido'),
    
    # Administração - Reservas
    path('admin/reservas/', views.lista_reservas, name='lista_reservas'),
]
