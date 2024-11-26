from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('livros/<int:pk>/', views.detalhes_livro, name='detalhes_livro'),
    path('livros/<int:pk>/emprestar/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
    path('meus-emprestimos/', views.meus_emprestimos, name='meus_emprestimos'),
    path('livros/<int:pk>/reservar/', views.criar_reserva, name='criar_reserva'),
    path('minhas-reservas/', views.minhas_reservas, name='minhas_reservas'),
    path('livros/<int:pk>/marcar_devolvido/', views.marcar_como_devolvido, name='marcar_como_devolvido'),
    path('login/', auth_views.LoginView.as_view(template_name='biblioteca/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

