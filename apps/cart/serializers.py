from rest_framework.serializers import ModelSerializer

from ..inventory.serializers import ProductoSerializer
from .models import Carrito


class CarritoSerializer(ModelSerializer):
    producto = ProductoSerializer(
        required=False,
        read_only=True,
        fields=("producto_id", "producto_nombre", "imagen", "precio"),
    )

    class Meta:
        model = Carrito
        fields = "__all__"
