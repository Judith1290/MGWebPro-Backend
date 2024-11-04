from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ..api.authentication import CookieAuthentication
from .models import Resena
from .serializers import ResenaSerializer


# CRUD de reseñas
@api_view(["GET", "POST", "PATCH"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def reviews_view(request, product_id=None, review_id=None):
    if request.method == "GET":
        # en caso de que se solicite una reseña en especifico.
        if review_id:
            instance = get_object_or_404(
                Resena, producto_id=product_id, resena_id=review_id
            )
            serializer = ResenaSerializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # se retornaran todas las reseñas del producto si no especifica una.
        instance = Resena.objects.filter(producto_id=product_id)
        serializer = ResenaSerializer(instance=instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ResenaSerializer(data=request.data)  # serialización de datos.
        if serializer.is_valid():  # validación de los datos.
            serializer.save(user_id=request.user.user_id, producto_id=product_id)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        # se busca en la db la reseña a editar.
        instance = get_object_or_404(Resena, resena_id=review_id)

        # se verifica que el usuario que haga la solicitud sea el autor.
        if not instance.user_id == request.user.user_id:
            # en caso de que no sea el autor.
            return Response(
                {"detail": "Only the review owner can edit it."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # se editan solamente los campos que se han recibido.
        serializer = ResenaSerializer(
            instance=instance, data=request.data, partial=True
        )
        if serializer.is_valid():  # validación de los datos.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
