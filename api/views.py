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
from .models import Carrito, Categoria, Modelo, Producto, Resena, Usuario
from .serializers import (
    CarritoSerializer,
    CategoriaSerializer,
    ModeloSerializer,
    ProductoSerializer,
    ResenaSerializer,
    UsuarioSerializer,
)

import hashlib
import hmac
import time
from django.http import JsonResponse
from django.conf import settings
from imagekitio import ImageKit
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def reviews_view(request, product_id=None, review_id=None):
    if request.method == "GET":
        if review_id:
            review = get_object_or_404(
                Resena, producto_id=product_id, resena_id=review_id
            )
            serializer = ResenaSerializer(instance=review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        reviews = Resena.objects.filter(producto_id=product_id)
        serializer = ResenaSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ResenaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.user_id, producto_id=product_id)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        review = get_object_or_404(Resena, resena_id=review_id)

        if not review.user_id == request.user.user_id:
            return Response(
                {"detail": "Only the review owner can edit it."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ResenaSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
def generate_imagekit_auth(request):
  
    imagekit = ImageKit(
        # private_key=settings.IMAGEKIT_PRIVATE_KEY,
        # public_key=settings.IMAGEKIT_PUBLIC_KEY,
        # url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
        
         private_key = 'private_vUdcFUmyKyVoaL8QNgLjrIIqfDg=' , 
         public_key = 'public_jQbYnV75+ohlENFlgG1cAyQdQA4=' , 
         url_endpoint =  'https://ik.imagekit.io/MGWebPro/'
    )
    
     
    auth_params = imagekit.get_authentication_parameters()

    return Response(auth_params)

@api_view(['PATCH', 'DELETE'])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail_view(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'PATCH':
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            usuario = request.user
            if usuario.rol_id == 1:  # Solo admin puede editar
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'No tienes permiso para editar productos.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        usuario = request.user
        if usuario.rol_id == 1:  # Solo admin puede eliminar
            producto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No tienes permiso para eliminar productos.'}, status=status.HTTP_403_FORBIDDEN)
    # actualizacion
@api_view(["POST"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart_view(request, pk=None):
    product = get_object_or_404(Producto, producto_id=pk)

    if not product.is_active:
        return Response(
            {"detail": "This product is not available"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if (product.stock - request.data["cantidad"]) < 0:
        return Response(
            {"detail": f"There is not enough stock. ({product.stock} remaining)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = CarritoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(producto_id=pk, user_id=request.user.user_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def user_cart_view(request, pk=None):
    if request.method == "GET":
        if pk:
            cart_product = get_object_or_404(
                Carrito, carrito_id=pk, user_id=request.user.user_id
            )
            serializer = CarritoSerializer(instance=cart_product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        cart_products = Carrito.objects.filter(user_id=request.user.user_id)
        serializer = CarritoSerializer(cart_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        cart_product = get_object_or_404(
            Carrito, carrito_id=pk, user_id=request.user.user_id
        )

        serializer = CarritoSerializer(cart_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        cart_product = get_object_or_404(
            Carrito, carrito_id=pk, user_id=request.user.user_id
        )
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
