from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, generics
from .models import Product, QuoteRequest, Category, Profile, Wishlist
from .serializers import ProductSerializer, QuoteRequestSerializer
from .forms import RegisterForm, ProfileForm

def get_wishlist_ids(request):
    if request.user.is_authenticated:
        return set(Wishlist.objects.filter(user=request.user).values_list("product_id", flat=True))
    return set()

def home(request):
    categories = Category.objects.all()
    return render(request, "home.html", {"categories": categories})

def shop_categories(request):
    categories = Category.objects.all()
    return render(request, "shop.html", {"categories": categories})

def shop_all_products(request):
    products = Product.objects.all()
    return render(request, "shop_products.html", {"products": products, "category": None, "wishlist_ids": get_wishlist_ids(request)})

def shop_category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, "shop_products.html", {"products": products, "category": category, "wishlist_ids": get_wishlist_ids(request)})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product, "wishlist_ids": get_wishlist_ids(request)})

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

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profile.html", {"form": form})

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    products = [item.product for item in items]
    return render(request, "wishlist.html", {"products": products, "wishlist_ids": get_wishlist_ids(request)})

@login_required
def wishlist_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    existing = Wishlist.objects.filter(user=request.user, product=product)
    if existing.exists():
        existing.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)
    next_url = request.POST.get("next") or "shop-list"
    return redirect(next_url)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class QuoteRequestCreateView(generics.CreateAPIView):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
