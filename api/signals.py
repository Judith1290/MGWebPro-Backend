from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Roles


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == "api":
        Roles.objects.get_or_create(
            nombre="Admin",
            rol_descripcion="Acceso total al sistema, puede gestionar usuarios, roles y productos",
        )
        Roles.objects.get_or_create(
            nombre="Moderador",
            rol_descripcion="Supervisa el contenido e interacciones, puede gestionar productos y usuarios",
        )
        Roles.objects.get_or_create(
            nombre="Usuario",
            rol_descripcion="Rol básico, puede realizar compras y enviar reseñas",
        )