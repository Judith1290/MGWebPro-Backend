import json

from imagekitio import ImageKit
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
