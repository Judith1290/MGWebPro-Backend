from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ..api.authentication import CookieAuthentication
from .models import Categoria, Modelo, Producto
from .serializers import CategoriaSerializer, ModeloSerializer, ProductoSerializer


# CRUD de productos
@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_view(request, pk=None):
    if request.method == "GET":
        # en caso de que se solicite un producto en especifico.
        if pk:
            instance = get_object_or_404(Producto, producto_id=pk)
            serializer = ProductoSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # se retornaran todos los productos si no especifica uno.
        instance = Producto.objects.all()
        serializer = ProductoSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # validación de que el usuario tenga los roles requeridos para realizar las siguientes acciones.
    if request.user.rol_id not in (1, 2):
        # en caso de que no cuente con los roles requeridos.
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "POST":
        serializer = ProductoSerializer(data=request.data)  # serialización de datos.
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        # se busca en la db el producto a editar.
        instance = get_object_or_404(Producto, producto_id=pk)

        # se editan solamente los campos que se han recibido.
        serializer = ProductoSerializer(
            instance=instance, data=request.data, partial=True
        )
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CRUD de modelos de productos.
@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_models_view(request, pk=None):
    if request.method == "GET":
        # en caso de que se solicite un modelo en especifico.
        if pk:
            instance = get_object_or_404(Modelo, modelo_id=pk)
            serializer = ModeloSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # se retornaran todos los modelos si no especifica uno.
        instance = Modelo.objects.all()
        serializer = ModeloSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # validación de que el usuario tenga los roles requeridos para realizar las siguientes acciones.
    if request.user.rol_id not in (1, 2):
        # en caso de que no cuente con los roles requeridos.
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "POST":
        serializer = ModeloSerializer(data=request.data)  # serialización de datos.
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        # se busca en la db el modelo a editar.
        instance = get_object_or_404(Modelo, modelo_id=pk)

        # se editan solamente los campos que se han recibido.
        serializer = ModeloSerializer(instance=instance, data=request.data)
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CRUD de categorias de productos.
@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_categories_view(request, pk=None):
    if request.method == "GET":
        # en caso de que se solicite una categoria en especifico.
        if pk:
            instance = get_object_or_404(Categoria, categoria_id=pk)
            serializer = CategoriaSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # se retornaran todas las categorias si no especifica una.
        instance = Categoria.objects.all()
        serializer = CategoriaSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # validación de que el usuario tenga los roles requeridos para realizar las siguientes acciones.
    if request.user.rol_id not in (1, 2):
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "POST":
        serializer = CategoriaSerializer(data=request.data)  # serialización de datos.
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        # se busca en la db la categoria a editar.
        instance = get_object_or_404(Categoria, categoria_id=pk)

        # se editan solamente los campos que se han recibido.
        serializer = CategoriaSerializer(instance=instance, data=request.data)
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def change_product_status_view(request, pk):
    if request.user.rol_id not in (1, 2):
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    product = get_object_or_404(Producto, producto_id=pk)
    product.is_active = not product.is_active
    product.save()
    return Response(status=status.HTTP_200_OK)