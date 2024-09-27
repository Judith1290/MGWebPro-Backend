import uuid
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .models import Usuario
from .serializers import UsuarioSerializer


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
