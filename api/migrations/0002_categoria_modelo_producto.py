# Generated by Django 5.1.1 on 2024-09-30 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('categoria_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('modelo_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_modelo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('producto_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('producto_nombre', models.CharField(max_length=150)),
                ('producto_descripcion', models.TextField()),
                ('imagen', models.TextField()),
                ('precio', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.categoria')),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.modelo')),
            ],
        ),
    ]