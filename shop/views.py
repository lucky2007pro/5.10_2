from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Product
from .serializers import ProductSerializer, ProductDetailAdminSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProductDetailAdminSerializer
        return ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        custom_response_data = {
            "success": True,
            "message": "Maxsulotlar ro'yxati muvaffaqiyatli olindi",
            "total_count": queryset.count(),
            "data": serializer.data
        }
        return Response(custom_response_data)


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailAdminSerializer

    def perform_update(self, serializer):
        price = serializer.validated_data.get('price', serializer.instance.price)
        stock = serializer.validated_data.get('stock', serializer.instance.stock)

        if price < 0:
            raise ValidationError("Narx manfiy bo'lishi mumkin emas!")

        instance = serializer.save()

        if instance.stock == 0 and instance.is_available:
            instance.is_available = False
            instance.save()
