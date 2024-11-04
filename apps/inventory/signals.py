from django.db.models.signals import post_migrate, pre_save
from django.dispatch import receiver

from .models import Categoria, Modelo, Producto


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


@receiver(pre_save, sender=Producto)
def update_product_status(sender, instance, **kwargs):
    if instance.pk:
        original = Producto.objects.get(producto_id=instance.pk)
        if original.stock > 0 and instance.stock == 0:
            instance.is_active = False
        elif original.stock == 0 and instance.stock > 0:
            instance.is_active = True
