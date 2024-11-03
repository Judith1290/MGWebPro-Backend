import ast
import uuid

from ..cart.models import Carrito
from ..inventory.models import Producto
from .serializers import ProductoFacturaSerializer, SimpleFacturaSerializer


# actualiza los productos y carrito
def update_products_and_cart_items(purchase_data):
    for e in purchase_data:
        product = Producto.objects.get(producto_id=e["product_id"])
        product.stock = product.stock - e["quantity"]
        product.save()

        if "cart_id" in e:
            cart = Carrito.objects.get(carrito_id=e["cart_id"])
            cart.delete()


# añade los datos de la factura a la db y retorna el id de esta misma
def create_invoice(metadata, payment_intent):
    purchase_data = ast.literal_eval(metadata["purchase_data"])

    data = {
        "user": uuid.UUID(metadata["user_id"]),
        "payment_intent_id": payment_intent,
    }
    serializer = SimpleFacturaSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        invoice_id = serializer.data["id"]

    for e in purchase_data:
        product = Producto.objects.get(producto_id=e["product_id"])
        data = {"precio": product.precio, "cantidad": e["quantity"]}
        serializer = ProductoFacturaSerializer(data=data)
        if serializer.is_valid():
            serializer.save(producto_id=product.producto_id, factura_id=invoice_id)

    return invoice_id
