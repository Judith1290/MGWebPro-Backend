import uuid
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .models import Producto, Usuario
from .serializers import ProductoSerializer, UsuarioSerializer
from .utils import has_permissions


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
            {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
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
    response.data = {"message": "Cookie deleted successfully"}
    return response


@api_view(["GET"])
def user_view(request):
    token = request.COOKIES.get("session")

    if not token:
        raise AuthenticationFailed("Unauthenticated")
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated")

    user = get_object_or_404(Usuario, user_id=uuid.UUID(payload["id"]))
    serializer = UsuarioSerializer(instance=user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "PATCH"])
def products_view(request, pk=None):
    token = request.COOKIES.get("session")

    if request.method == "GET":
        if pk:
            product = get_object_or_404(Producto, producto_id=pk)
            serializer = ProductoSerializer(instance=product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        products = Producto.objects.all()
        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not has_permissions(token=token, roles=(1, 2)):
            return Response(
                {"error": "You do not have permissions to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        if not has_permissions(token=token, roles=(1, 2)):
            return Response(
                {"error": "You do not have permissions to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(Producto, producto_id=pk)
        serializer = ProductoSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
