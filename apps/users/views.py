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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..api.authentication import CookieAuthentication
from .models import Usuario
from .serializers import UsuarioSerializer


@api_view(["POST"])
def register_view(request):
    serializer = UsuarioSerializer(data=request.data)

    if serializer.is_valid():  # validación de los datos.
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):
    # busqueda del usuario por el email recibido.
    user = get_object_or_404(Usuario, email=request.data["email"])

    # comparación de la contraseña de la db con la recibida.
    if not user.check_password(request.data["password"]):
        # en caso de que las contraseñas no coincidan.
        return Response(
            {"detail": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )

    # creación y encriptación del token de sesión.
    payload = {
        "id": str(user.user_id),
        "exp": datetime.now() + timedelta(days=56),
        "iat": datetime.now(),
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")

    response = Response(status=status.HTTP_200_OK)
    # el token se guarda en la cookie `session`.
    response.set_cookie(key="session", value=token, httponly=True)
    update_last_login(None, user)
    return response


@api_view(["POST"])
def logout_view(request):  # se cierra la sesión eliminando la cookie `session`
    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie("session")
    response.data = {"detail": "Cookie deleted successfully"}
    return response


@api_view(["GET"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    # se retornan los datos del usuario logeado
    serializer = UsuarioSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
