from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # 1. get_queryset funksiyasini override qilish
    # Maqsad: Faqatgina joriy tizimga kirgan foydalanuvchiga tegishli vazifalarni qaytarish
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user, is_active=True)

    # 2. perform_create funksiyasini override qilish
    # Maqsad: Yangi vazifa yaratilayotganda uni so'rov yuborgan foydalanuvchiga (owner) avtomatik biriktirish
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    # Obyektni izlashda faqat joriy foydalanuvchining aktiv vazifalari ichidan qidirish
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user, is_active=True)

    # 3. perform_destroy funksiyasini override qilish
    # Maqsad: Obyektni ma'lumotlar bazasidan butunlay o'chirmasdan, uning statusini o'zgartirish (Soft delete)
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
