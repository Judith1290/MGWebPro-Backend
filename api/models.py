import uuid

from django.db import models


# Create your models here.
class Roles(models.Model):
    rol_id = models.AutoField(primary_key=True)
    rol_descripcion = models.TextField()


class Usuario(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    contrasena = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol_id = models.ForeignKey(Roles, on_delete=models.PROTECT, default=3)
