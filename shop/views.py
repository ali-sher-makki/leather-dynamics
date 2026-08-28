from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from .models import Product, ContactMessage
from .serializers import ProductSerializer, ContactMessageSerializer

def home(request):
    return render(request, "home.html")

def shop_list(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
