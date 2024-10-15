# Generated by Django 5.1.1 on 2024-10-15 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('carrito_id', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.producto')),
            ],
        ),
    ]
