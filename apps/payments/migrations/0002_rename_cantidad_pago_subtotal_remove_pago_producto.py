# Generated by Django 5.1.1 on 2024-10-28 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago',
            old_name='cantidad',
            new_name='subtotal',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='producto',
        ),
    ]
