# Generated by Django 5.2 on 2025-04-09 17:25

import django.db.models.deletion
import django.utils.timezone
import users.models.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20)),
                ('foto_anverso', models.ImageField(blank=True, null=True, upload_to=users.models.models.visita_foto_path, verbose_name='Foto Anverso de Cédula')),
                ('foto_reverso', models.ImageField(blank=True, null=True, upload_to=users.models.models.visita_foto_path, verbose_name='Foto Reverso de Cédula')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateTimeField(default=django.utils.timezone.now)),
                ('hora_entrada', models.TimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.visita')),
            ],
        ),
    ]
