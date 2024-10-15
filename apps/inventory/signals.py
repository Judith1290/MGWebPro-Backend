from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Categoria, Modelo


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == "apps.inventory":
        Categoria.objects.get_or_create(nombre_categoria="Cargadores")
        Categoria.objects.get_or_create(nombre_categoria="Cables USB")
        Categoria.objects.get_or_create(nombre_categoria="Cubos")
        Categoria.objects.get_or_create(nombre_categoria="Temperados")
        Categoria.objects.get_or_create(nombre_categoria="Aros de luz")
        Categoria.objects.get_or_create(nombre_categoria="Audifonos")
        Categoria.objects.get_or_create(nombre_categoria="Celulares")
        Categoria.objects.get_or_create(nombre_categoria="Figuras")


@receiver(post_migrate)
def create_default_models(sender, **kwargs):
    if sender.name == "apps.inventory":
        Modelo.objects.get_or_create(nombre_modelo="Samsung")
        Modelo.objects.get_or_create(nombre_modelo="Huawei")
        Modelo.objects.get_or_create(nombre_modelo="iPhone")
        Modelo.objects.get_or_create(nombre_modelo="Xiaomi")
