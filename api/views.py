# type: ignore
from rest_framework.viewsets import ModelViewSet

from .models import Usuario
from .serializers import UsuarioSerializer

# Create your views here.


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build # type: ignore
from googleapiclient.errors import HttpError # type: ignore
import google.auth # type: ignore



from .models import Categoria, Modelo, Producto, Usuario
from .serializers import (
    CategoriaSerializer,
    ModeloSerializer,
    ProductoSerializer,
    UsuarioSerializer,
)
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


@api_view(["GET", "POST", "PATCH"])
def products_models_view(request, pk=None):
    token = request.COOKIES.get("session")

    if request.method == "GET":
        if pk:
            model = get_object_or_404(Modelo, modelo_id=pk)
            serializer = ModeloSerializer(instance=model)
            return Response(serializer.data, status=status.HTTP_200_OK)

        models = Modelo.objects.all()
        serializer = ModeloSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not has_permissions(token=token, roles=(1, 2)):
            return Response(
                {"error": "You do not have permissions to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ModeloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        if not has_permissions(token=token, roles=(1, 2)):
            return Response(
                {"error": "You do not have permissions to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        model = get_object_or_404(Modelo, modelo_id=pk)
        serializer = ModeloSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "POST", "PATCH"])
def products_categories_view(request, pk=None):
    token = request.COOKIES.get("session")

    if request.method == "GET":
        if pk:
            category = get_object_or_404(Categoria, categoria_id=pk)
            serializer = CategoriaSerializer(instance=category)
            return Response(serializer.data, status=status.HTTP_200_OK)

        categories = Categoria.objects.all()
        serializer = CategoriaSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not has_permissions(token=token, roles=(1, 2)):
            return Response(
                {"error": "You do not have permissions to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        if not has_permissions(token=token, roles=(1, 2)):
            return Response(
                {"error": "You do not have permissions to perform this action"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        category = get_object_or_404(Categoria, categoria_id=pk)
        serializer = CategoriaSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# @api_view(["POST"])
# def send_email(request):
    
    
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         name = data.get('name')
#         email = data.get('email')
#         numero_phone = data.get('numero_phone')
#         message = data.get('message')

#         try:
           
#             send_mail(
#                 subject=f"Mensaje de {name}",
#                 message=f"Teléfono: {numero_phone}\n\nMensaje: {message}",
#                 from_email=email,
#                 recipient_list=['mgtechnology.crp@gmail.com'],
#                 fail_silently=False,
#             )
#             return JsonResponse({'status': 'Correo enviado exitosamente'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def send_email(request):
    print(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Obtener los datos del formulario
        name = data['name']
        email = data['email']
        phone = data['phone']
        message_text = data['message']
        
        # Aquí puedes usar la función para enviar el correo
        try:
            creds, _ = google.auth.default()
            service = build("gmail", "v1", credentials=creds)

            # Crear mensaje de correo
            message = EmailMessage()
            message.set_content(f"Nombre: {name}\nEmail: {email}\nTeléfono: {phone}\n\nMensaje:\n{message_text}")
            message["To"] = "tucorreo@example.com"  # Tu correo
            message["From"] = "tuotrocorreo@example.com"
            message["Subject"] = "Nuevo mensaje de contacto"

            # Codificar el mensaje
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}

            # Enviar el correo
            send_message = service.users().messages().send(userId="me", body=create_message).execute()

            return JsonResponse({"success": True, "message": "Correo enviado exitosamente."})

        except HttpError as error:
            print(f"Error al enviar el correo: {error}")
            return JsonResponse({"success": False, "message": "Error al enviar el correo."})

    return JsonResponse({"success": False, "message": "Método no permitido."})


       
              
           
