from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Product
from .serializers import ProductSerializer, ProductDetailAdminSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)

    # 1. get_serializer_class funksiyasini override qilish
    # Maqsad: Agar foydalanuvchi admin bo'lsa, to'liq ma'lumotli serializerni qaytarish, oddiy foydalanuvchi uchun boshqasini
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ProductDetailAdminSerializer
        return ProductSerializer

    # 2. list funksiyasini override qilish
    # Maqsad: Javobga qo'shimcha maxsus metadata (total_count, message) qo'shib yuborish
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

    # 3. perform_update funksiyasini override qilish
    # Maqsad: Maxsulot yangilanayotganda maxsus validatsiya kiritish (masalan, narx manfiy bo'lishini tekshirish) 
    # va qoldiq zaxirani (stock) tekshirish
    def perform_update(self, serializer):
        price = serializer.validated_data.get('price', serializer.instance.price)
        stock = serializer.validated_data.get('stock', serializer.instance.stock)
        
        if price < 0:
            raise ValidationError("Narx manfiy bo'lishi mumkin emas!")
            
        # O'zgarishni saqlash
        instance = serializer.save()
        
        # Agar zaxira tugasa, maxsulotni mavjud emas (unavailable) qilib belgilash
        if instance.stock == 0 and instance.is_available:
            instance.is_available = False
            instance.save()
