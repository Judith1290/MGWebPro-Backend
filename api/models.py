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
    # imagen = models.TextField()
    imagen = models.URLField(max_length=200, blank=True, null=True) 
    precio = models.IntegerField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, null=True)


class Resena(models.Model):
    resena_id = models.AutoField(primary_key=True)
    comentario = models.TextField()
    calificacion = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)


class Carrito(models.Model):
    carrito_id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
