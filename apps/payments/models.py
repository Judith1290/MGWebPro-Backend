from django.db import models

from ..inventory.models import Producto
from ..users.models import Usuario


class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField()
    stripe_checkout_id = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
