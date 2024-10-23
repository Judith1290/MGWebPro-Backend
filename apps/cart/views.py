from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..api.authentication import CookieAuthentication
from ..inventory.models import Producto
from .models import Carrito
from .serializers import CarritoSerializer


@api_view(["POST"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart_view(request, pk=None):
    # se obtiene el producto para realizar validaciones.
    product = get_object_or_404(Producto, producto_id=pk)

    if not product.is_active:  # se verifica que el producto esté activo.
        return Response(
            {"detail": "This product is not available"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # se comprueba que haya stock suficiente.
    if (product.stock - request.data["cantidad"]) < 0:
        return Response(
            {"detail": f"There is not enough stock. ({product.stock} remaining)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = CarritoSerializer(data=request.data)  # se serializan los datos.
    if serializer.is_valid():  # se validan los datos.
        serializer.save(producto_id=pk, user_id=request.user.user_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def user_cart_view(request, pk=None):
    if request.method == "GET":
        # en caso de que se solicite un producto del carrito en especifico.
        if pk:
            instance = get_object_or_404(
                Carrito, carrito_id=pk, user_id=request.user.user_id
            )
            serializer = CarritoSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # se retornaran todos los productos del carrito si no especifica uno.
        instance = Carrito.objects.filter(user_id=request.user.user_id)
        serializer = CarritoSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        # se busca en la db el producto de carrito a editar.
        instance = get_object_or_404(
            Carrito, carrito_id=pk, user_id=request.user.user_id
        )

        product = get_object_or_404(Producto, producto_id=instance.producto.producto_id)
        # se comprueba que haya stock suficiente.
        if (product.stock - request.data["cantidad"]) < 0:
            return Response(
                {"detail": f"There is not enough stock. ({product.stock} remaining)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # se editan solamente los campos que se han recibido (cantidad, lol).
        serializer = CarritoSerializer(
            instance=instance, data=request.data, partial=True
        )
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        # se busca en la db el producto de carrito a eliminar.
        instance = get_object_or_404(
            Carrito, carrito_id=pk, user_id=request.user.user_id
        )
        instance.delete()  # se elimina lol
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
