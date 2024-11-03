import base64

import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException


def send_email(
    subject,
    html_content,
    to,
    reply_to=settings.SENDER_EMAIL,
    attachment=None,
    attch_name=None,
):
    # Configurar la clave de la API de Brevo
    api_key = settings.BREVO_SECRET_KEY

    # Crear una instancia de la API con la configuración
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key

    # Crear el cliente de la API
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # Configurar el contenido del correo
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender={"name": "MG Technology", "email": settings.SENDER_EMAIL},
        subject=subject,
        html_content=html_content,
        reply_to={"email": reply_to},
    )

    if attachment and attch_name:
        attch_b64 = base64.b64encode(attachment).decode("utf-8")
        send_smtp_email.attachment = [{"content": attch_b64, "name": attch_name}]

    try:
        # Llamada a la API para enviar el correo
        api_instance.send_transac_email(send_smtp_email)
        return {"message": "Correo enviado con éxito"}
    except ApiException as e:
        # Capturar y mostrar el error detallado
        error_message = e.body if e.body else str(e)
        return {"error": f"Error al enviar correo: {error_message}"}
