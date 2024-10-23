from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..inventory.serializers import ProductoSerializer
from .models import Pago


class PagoSerializer(ModelSerializer):
    producto = ProductoSerializer(
        required=False,
        read_only=True,
        fields=("producto_id", "nombre", "precio", "imagen"),
    )
    sub_total = SerializerMethodField(method_name="get_total")

    class Meta:
        model = Pago
        fields = "__all__"

    def get_total(self, pago: Pago):
        return pago.producto.precio * pago.cantidad
