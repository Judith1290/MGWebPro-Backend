import json

from imagekitio import ImageKit
from rest_framework.decorators import api_view
from rest_framework.response import Response
import sib_api_v3_sdk 
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from .serializers.contact import ContactSerializer
from rest_framework import status

@api_view(["GET"])
def generate_imagekit_auth(request):
    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    imagekit = ImageKit(
        private_key=secrets["IMAGEKIT_PRIVATE_KEY"],
        public_key=secrets["IMAGEKIT_PUBLIC_KEY"],
        url_endpoint=secrets["IMAGEKIT_URL_ENDPOINT"],
    )

    auth_params = imagekit.get_authentication_parameters()
    return Response(auth_params)

@api_view(["POST"])
def enviar_correo(request):
     # Imprimir mensaje de depuración
        print("Procesando solicitud para enviar correo...")

        # Configurar la clave de la API de Brevo
        api_key = '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'  # Reemplaza con tu API Key válida de Brevo

        # Crear una instancia de la API con la configuración
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key

        # Crear el cliente de la API
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Serializar los datos del request
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            # Obtener los datos del request
            email_destino = serializer.validated_data.get('email')
            contenido_html = serializer.validated_data.get('message')

            # Configurar el contenido del correo
            email_origen = {
                "name": "Prueba",
                "email": "marijudith.garcia@gmail.com"  # Reemplaza con tu correo de origen
            }

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": email_destino}],
                sender=email_origen,
                subject="Asunto",
                html_content=contenido_html
            )

            try:
                # Llamada a la API para enviar el correo
                api_response = api_instance.send_transac_email(send_smtp_email)
                print("Respuesta de la API:", api_response)
                return Response({"message": "Correo enviado con éxito"}, status=status.HTTP_200_OK)
            except ApiException as e:
                # Capturar y mostrar el error detallado
                error_message = e.body if e.body else str(e)
                print(f"Error al enviar correo: {error_message}")
                return Response({"error": f"Error al enviar correo: {error_message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Si los datos no son válidos, devolver errores de validación
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)