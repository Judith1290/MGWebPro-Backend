from rest_framework.serializers import ModelSerializer

from ..users.serializers import UsuarioSerializer
from .models import Resena


class ResenaSerializer(ModelSerializer):
    user = UsuarioSerializer(
        required=False, read_only=True, fields=("first_name", "last_name")
    )

    class Meta:
        model = Resena
        fields = "__all__"
