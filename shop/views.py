from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics
from .models import Product, QuoteRequest
from .serializers import ProductSerializer, QuoteRequestSerializer

def home(request):
    return render(request, "home.html")

def shop_list(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

def contact_page(request):
    return render(request, "contact.html")

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class QuoteRequestCreateView(generics.CreateAPIView):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
