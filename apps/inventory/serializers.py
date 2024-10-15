from rest_framework.serializers import ModelSerializer

from ..api.utils import DynamicFieldsModelSerializer
from .models import Categoria, Modelo, Producto


class ModeloSerializer(ModelSerializer):
    class Meta:
        model = Modelo
        fields = "__all__"


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ProductoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
