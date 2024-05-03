from rest_framework import serializers
from django.conf import settings
from .models import Cart, CartItem, Producto

class ProductoSerializer(serializers.ModelSerializer):
    imagen_producto_url = serializers.SerializerMethodField()
    tipo_nombre = serializers.CharField(source='tipo.nombre', read_only=True)  # Asume que 'tipo' es una relación ForeignKey


    class Meta:
        model = Producto
        fields = ['id', 'descripcion', 'precio', 'imagen_producto_url', 'tipo_nombre']  # Incluye el nuevo campo 'tipo_nombre'

    def get_imagen_producto_url(self, obj):
        request = self.context.get('request')
        if obj.imagen_producto:
            return request.build_absolute_uri(obj.imagen_producto.url)
        return None

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductoSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
