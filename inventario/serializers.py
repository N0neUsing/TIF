from rest_framework import serializers
from django.conf import settings
from .models import Cart, CartItem, Producto

class ProductoSerializer(serializers.ModelSerializer):
    imagen_producto_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'descripcion', 'precio', 'imagen_producto_url']  # Incluye el nuevo campo imagen_producto_url

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
