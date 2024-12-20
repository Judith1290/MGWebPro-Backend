# Generated by Django 5.1.1 on 2024-10-15 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('imagen', models.URLField(blank=True, null=True)),
                ('precio', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.categoria')),
                ('modelo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.modelo')),
            ],
        ),
    ]
