import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    rol_descripcion = models.TextField()

class Usuario(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    rol = models.ForeignKey(Roles, on_delete=models.PROTECT, default=3)
    username = None
    is_superuser = None
    is_staff = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)


class Modelo(models.Model):
    modelo_id = models.AutoField(primary_key=True)
    nombre_modelo = models.CharField(max_length=50)


class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True, unique=True)
    producto_nombre = models.CharField(max_length=150)
    producto_descripcion = models.TextField()
    imagen = models.TextField()
    precio = models.IntegerField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, null=True)

class EmailCliend(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=12)
    phone = models.CharField(max_length=20)
    masagge = models.TextField()
