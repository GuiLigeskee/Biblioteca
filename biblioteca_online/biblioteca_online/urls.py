from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('biblioteca.urls')),  # Inclui as rotas do app biblioteca
]
