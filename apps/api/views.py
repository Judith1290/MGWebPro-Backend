from django.conf import settings
from imagekitio import ImageKit
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.email_utils import send_email

from .serializers.contact import ContactSerializer


@api_view(["GET"])
def generate_imagekit_auth(request):
    imagekit = ImageKit(
        private_key=settings.IMAGEKIT_PRIVATE_KEY,
        public_key=settings.IMAGEKIT_PUBLIC_KEY,
        url_endpoint=settings.IMAGEKIT_URL_ENDPOINT,
    )

    auth_params = imagekit.get_authentication_parameters()
    return Response(auth_params)


@api_view(["POST"])
def enviar_correo(request):
    # Serializar los datos del request
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        # Obtener los datos del request
        email_destino = serializer.validated_data.get("email")
        contenido_html = serializer.validated_data.get("message")

        response = send_email(
            to=[{"email": settings.SENDER_EMAIL}],
            reply_to=email_destino,
            subject="Contacto",
            html_content=contenido_html,
        )

        if "message" in response:
            return Response(response, status=status.HTTP_200_OK)
        elif "error" in response:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Si los datos no son válidos, devolver errores de validación
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
