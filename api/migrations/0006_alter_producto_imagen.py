# Generated by Django 5.1.1 on 2024-10-10 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_resena_producto_alter_resena_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.URLField(max_length=500),
        ),
    ]