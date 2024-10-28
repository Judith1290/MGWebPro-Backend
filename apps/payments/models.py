from django.db import models

from ..users.models import Usuario


class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    subtotal = models.IntegerField()
    payment_intent_id = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
