import uuid

import jwt
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed

from .models import Usuario


def has_permissions(token: str, roles: tuple) -> bool:
    if not token:
        raise AuthenticationFailed("Unauthenticated")
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated")

    user = get_object_or_404(Usuario, user_id=uuid.UUID(payload["id"]))

    if user.rol_id not in roles:
        return False

    return True
