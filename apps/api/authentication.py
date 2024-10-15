import uuid

import jwt
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from ..users.models import Usuario


class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("session")

        if not token:
            return None

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as error:
            raise AuthenticationFailed({"detail": error})

        user = get_object_or_404(Usuario, user_id=uuid.UUID(payload["id"]))

        return (user, None)
