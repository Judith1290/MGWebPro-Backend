from utils.serializers import DynamicFieldsModelSerializer
from .models import Usuario


class UsuarioSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["rol_id"] = 3  # asignación del rol por defecto
        # hasheo de contraseña
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)

        user.save()
        return user
