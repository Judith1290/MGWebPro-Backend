from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .authentication import CookieAuthentication
from .models import Categoria, Modelo, Producto, Resena, Usuario
from .serializers import (
    CategoriaSerializer,
    ModeloSerializer,
    ProductoSerializer,
    ResenaSerializer,
    UsuarioSerializer,
)


@api_view(["POST"])
def register_view(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):
    user = get_object_or_404(Usuario, email=request.data["email"])

    if not user.check_password(request.data["password"]):
        return Response(
            {"detail": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )

    payload = {
        "id": str(user.user_id),
        "exp": datetime.now() + timedelta(days=56),
        "iat": datetime.now(),
    }

    token = jwt.encode(payload, "secret", algorithm="HS256")

    response = Response(status=status.HTTP_200_OK)
    response.set_cookie(key="session", value=token, httponly=True)
    update_last_login(None, user)
    return response


@api_view(["POST"])
def logout_view(request):
    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie("session")
    response.data = {"detail": "Cookie deleted successfully"}
    return response


@api_view(["GET"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    serializer = UsuarioSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_view(request, pk=None):
    if request.method == "GET":
        if pk:
            product = get_object_or_404(Producto, producto_id=pk)
            serializer = ProductoSerializer(instance=product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        products = Producto.objects.all()
        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.user.rol_id not in (1, 2):
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "POST":
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        product = get_object_or_404(Producto, producto_id=pk)
        serializer = ProductoSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_models_view(request, pk=None):
    if request.method == "GET":
        if pk:
            model = get_object_or_404(Modelo, modelo_id=pk)
            serializer = ModeloSerializer(instance=model)
            return Response(serializer.data, status=status.HTTP_200_OK)

        models = Modelo.objects.all()
        serializer = ModeloSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.user.rol_id not in (1, 2):
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "POST":
        serializer = ModeloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        model = get_object_or_404(Modelo, modelo_id=pk)
        serializer = ModeloSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def products_categories_view(request, pk=None):
    if request.method == "GET":
        if pk:
            category = get_object_or_404(Categoria, categoria_id=pk)
            serializer = CategoriaSerializer(instance=category)
            return Response(serializer.data, status=status.HTTP_200_OK)

        categories = Categoria.objects.all()
        serializer = CategoriaSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.user.rol_id not in (1, 2):
        return Response(
            {"detail": "You do not have permissions to perform this action."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "POST":
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        category = get_object_or_404(Categoria, categoria_id=pk)
        serializer = CategoriaSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
