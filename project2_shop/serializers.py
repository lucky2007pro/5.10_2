from rest_framework import serializers
from .models import Product

# Umumiy ma'lumotlar uchun (Mijozlar)
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name', 'is_available']

# Adminlar uchun to'liq ma'lumotli serializer
class ProductDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
