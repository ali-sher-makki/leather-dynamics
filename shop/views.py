from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, generics
from .models import Product, QuoteRequest, Category, Profile, Wishlist, CartItem, Order, OrderItem
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
    orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")
    return render(request, "profile.html", {"form": form, "orders": orders})

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

@login_required
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.price:
        messages.error(request, "This product needs a custom quote - please use Request a Quote instead.")
        return redirect("product-page", pk=pk)
    qty = request.POST.get("quantity", "1")
    qty = int(qty) if qty.isdigit() and int(qty) > 0 else 1
    item, created = CartItem.objects.get_or_create(user=request.user, product=product, defaults={"quantity": qty})
    if not created:
        item.quantity += qty
        item.save()
    messages.success(request, f"{product.name} added to cart.")
    next_url = request.POST.get("next") or "cart"
    return redirect(next_url)

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.subtotal() for item in items)
    return render(request, "cart.html", {"items": items, "total": total})

@login_required
def cart_update(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    qty = request.POST.get("quantity", "1")
    if qty.isdigit() and int(qty) > 0:
        item.quantity = int(qty)
        item.save()
    else:
        item.delete()
    return redirect("cart")

@login_required
def cart_remove(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    return redirect("cart")

@login_required
def checkout_view(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    if not items.exists():
        return redirect("cart")
    total = sum(item.subtotal() for item in items)
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name", ""),
            phone=request.POST.get("phone", ""),
            address=request.POST.get("address", ""),
            city=request.POST.get("city", ""),
            country=request.POST.get("country", ""),
            notes=request.POST.get("notes", ""),
            total_amount=total,
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
        items.delete()
        return redirect("order-confirmation", pk=order.id)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "checkout.html", {"items": items, "total": total, "profile": profile})

@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "order_confirmation.html", {"order": order})

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class QuoteRequestCreateView(generics.CreateAPIView):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
