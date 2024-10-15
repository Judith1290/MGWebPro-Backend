from django.db import models

from ..inventory.models import Producto
from ..users.models import Usuario


class Carrito(models.Model):
    carrito_id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
