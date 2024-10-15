from django.db import models

from ..inventory.models import Producto
from ..users.models import Usuario


class Resena(models.Model):
    resena_id = models.AutoField(primary_key=True)
    comentario = models.TextField()
    calificacion = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
