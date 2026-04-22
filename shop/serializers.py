from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name', 'is_available']


class ProductDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
