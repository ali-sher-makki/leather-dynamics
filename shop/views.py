from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Product, ContactMessage
from .serializers import ProductSerializer, ContactMessageSerializer

def home(request):
    return render(request, "home.html")

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
