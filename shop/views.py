from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Product
from .serializers import ProductSerializer, ProductDetailAdminSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.user.is_staff:
            return ProductDetailAdminSerializer
        return ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": "Maxsulotlar ro'yxati",
            "total_count": queryset.count(),
            "data": serializer.data
        })

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailAdminSerializer

    def perform_update(self, serializer):
        price = serializer.validated_data.get('price', serializer.instance.price)
        if price is not None and price < 0:
            raise ValidationError("Narx manfiy bo'lishi mumkin emas!")

        instance = serializer.save()

        if instance.stock == 0 and instance.is_available:
            instance.is_available = False
            instance.save()