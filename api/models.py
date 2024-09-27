import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    rol_descripcion = models.TextField()


class Usuario(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    rol = models.ForeignKey(Roles, on_delete=models.PROTECT, default=3)
    username = None
    is_superuser = None
    is_staff = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
