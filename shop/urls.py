from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListCreateView.as_view()),
    path('update<int:pk>/', ProductDetailView.as_view()),
]

