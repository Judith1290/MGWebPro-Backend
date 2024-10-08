from rest_framework.serializers import ModelSerializer

from .models import Categoria, Modelo, Producto, Usuario, EmailCliend


class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)

        user.save()
        return user


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"


class ModeloSerializer(ModelSerializer):
    class Meta:
        model = Modelo
        fields = "__all__"


class CategoriaSerializer(ModeloSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
        
class SendEmailSerializer(ModelSerializer):
    class Meta:
        model = EmailCliend
        fields = "__all__"
