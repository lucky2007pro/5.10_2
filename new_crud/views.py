from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import ProductSerializer, UserSerializer, CategorySerializer
from .models import Product, User, Category
# Create your views here.

class Products(ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
