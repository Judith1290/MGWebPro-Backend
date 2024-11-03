from django.db import models

from ..inventory.models import Producto
from ..users.models import Usuario


class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    payment_intent_id = models.CharField(max_length=500)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class ProductoFactura(models.Model):
    id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="productos", null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    precio = models.IntegerField()
    cantidad = models.IntegerField()

    def get_total(self):
        return self.precio * self.cantidad
