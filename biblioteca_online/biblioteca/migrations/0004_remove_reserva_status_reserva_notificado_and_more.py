# Generated by Django 5.1.3 on 2024-11-26 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0003_alter_reserva_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='status',
        ),
        migrations.AddField(
            model_name='reserva',
            name='notificado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='data_reserva',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]