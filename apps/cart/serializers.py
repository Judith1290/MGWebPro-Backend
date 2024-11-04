from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..inventory.serializers import ProductoSerializer
from .models import Carrito


class CarritoSerializer(ModelSerializer):
    producto = ProductoSerializer(
        required=False,
        read_only=True,
        fields=("producto_id", "nombre", "descripcion", "imagen", "precio"),
    )
    sub_total = SerializerMethodField(method_name="get_total")

    class Meta:
        model = Carrito
        fields = ["carrito_id", "producto", "cantidad", "sub_total"]

    def get_total(self, cart_item: Carrito):
        return cart_item.producto.precio * cart_item.cantidad
