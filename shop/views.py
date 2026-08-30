from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from rest_framework import viewsets, generics
from .models import Product, QuoteRequest, Category
from .serializers import ProductSerializer, QuoteRequestSerializer
from .forms import RegisterForm

def home(request):
    categories = Category.objects.all()
    return render(request, "home.html", {"categories": categories})

def shop_categories(request):
    categories = Category.objects.all()
    return render(request, "shop.html", {"categories": categories})

def shop_all_products(request):
    products = Product.objects.all()
    return render(request, "shop_products.html", {"products": products, "category": None})

def shop_category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, "shop_products.html", {"products": products, "category": category})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

def contact_page(request):
    return render(request, "contact.html")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.company_name = form.cleaned_data.get("company_name", "")
            user.profile.country = form.cleaned_data.get("country", "")
            user.profile.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class QuoteRequestCreateView(generics.CreateAPIView):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
