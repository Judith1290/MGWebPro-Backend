from django.db import models


class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)


class Modelo(models.Model):
    modelo_id = models.AutoField(primary_key=True)
    nombre_modelo = models.CharField(max_length=50)


class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.URLField(max_length=200, blank=True, null=True)
    precio = models.IntegerField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, blank=True, null=True)
