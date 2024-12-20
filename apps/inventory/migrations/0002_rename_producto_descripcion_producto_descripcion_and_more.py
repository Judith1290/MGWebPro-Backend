# Generated by Django 5.1.1 on 2024-10-18 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='producto_descripcion',
            new_name='descripcion',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='producto_nombre',
            new_name='nombre',
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.categoria'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='modelo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.modelo'),
        ),
    ]
