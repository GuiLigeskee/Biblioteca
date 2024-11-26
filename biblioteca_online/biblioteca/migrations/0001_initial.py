# Generated by Django 5.1.3 on 2024-11-26 13:07

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=100)),
                ('genero', models.CharField(max_length=50)),
                ('disponivel', models.BooleanField(default=True)),
                ('data_publicacao', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_emprestimo', models.DateField(auto_now_add=True)),
                ('data_devolucao', models.DateField(default=datetime.date(2024, 12, 10))),
                ('devolvido', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.livro')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_reserva', models.DateField(auto_now_add=True)),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.livro')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]