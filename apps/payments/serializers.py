from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..inventory.serializers import ProductoSerializer
from .models import Factura, ProductoFactura


class SimpleFacturaSerializer(ModelSerializer):
    class Meta:
        model = Factura
        fields = "__all__"


class ProductoFacturaSerializer(ModelSerializer):
    producto = ProductoSerializer(
        required=False, read_only=True, fields=("nombre", "imagen")
    )
    total = SerializerMethodField(method_name="get_total")

    class Meta:
        model = ProductoFactura
        fields = ["producto", "precio", "cantidad", "total"]

    def get_total(self, item: ProductoFactura):
        return item.precio * item.cantidad


class FacturaSerializer(ModelSerializer):
    productos = ProductoFacturaSerializer(many=True)
    subtotal = SerializerMethodField(method_name="get_subtotal")

    class Meta:
        model = Factura
        fields = ["payment_intent_id", "productos", "subtotal", "fecha_creacion"]

    def get_subtotal(self, factura: Factura):
        productos = factura.productos.all()
        total = sum([producto.cantidad * producto.precio for producto in productos])
        return total
