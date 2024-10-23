from django.conf import settings
from imagekitio import ImageKit
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def generate_imagekit_auth(request):
    imagekit = ImageKit(
        private_key=settings.IMAGEKIT_PRIVATE_KEY,
        public_key=settings.IMAGEKIT_PUBLIC_KEY,
        url_endpoint=settings.IMAGEKIT_URL_ENDPOINT,
    )

    auth_params = imagekit.get_authentication_parameters()
    return Response(auth_params)
