# Generated by Django 5.1.1 on 2024-10-08 02:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_resena'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resena',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.producto'),
        ),
        migrations.AlterField(
            model_name='resena',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]