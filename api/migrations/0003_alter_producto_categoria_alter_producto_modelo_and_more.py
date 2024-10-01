# Generated by Django 5.1.1 on 2024-10-01 17:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_categoria_modelo_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.categoria'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='modelo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.modelo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]