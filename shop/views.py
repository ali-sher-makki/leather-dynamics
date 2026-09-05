from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.db.models import Avg
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import viewsets, generics
from .models import Product, QuoteRequest, Category, Profile, Wishlist, CartItem, Order, OrderItem, Review
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
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "shop_products.html", {"products": products, "category": None, "wishlist_ids": get_wishlist_ids(request), "search_query": query})

def shop_category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "shop_products.html", {"products": products, "category": category, "wishlist_ids": get_wishlist_ids(request), "search_query": query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]
    user_review = None
    has_delivered_order = False
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        has_delivered_order = OrderItem.objects.filter(
            product=product, order__user=request.user, order__status="delivered"
        ).exists()

    if request.method == "POST" and request.user.is_authenticated and not user_review and has_delivered_order:
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            Review.objects.create(product=product, user=request.user, rating=int(rating), comment=comment)
            messages.success(request, "Thanks for your review!")
            return redirect("product-page", pk=pk)

    return render(request, "product_detail.html", {
        "product": product,
        "wishlist_ids": get_wishlist_ids(request),
        "reviews": reviews,
        "avg_rating": avg_rating,
        "user_review": user_review,
        "has_delivered_order": has_delivered_order,
    })

def contact_page(request):
    return render(request, "contact.html")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile.company_name = form.cleaned_data.get("company_name", "")
            user.profile.country = form.cleaned_data.get("country", "")
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                user.profile.avatar = avatar
            user.profile.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    editing = request.GET.get("edit") == "1"
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
        editing = True
    else:
        form = ProfileForm(instance=profile)
    recent_orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")[:3]
    return render(request, "profile.html", {"form": form, "orders": recent_orders, "editing": editing, "profile": profile})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")
    return render(request, "order_history.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, "order_detail.html", {"order": order})

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    products = [item.product for item in items]
    return render(request, "wishlist.html", {"products": products, "wishlist_ids": get_wishlist_ids(request)})

def wishlist_toggle(request, pk):
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse("home")
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to save items to your wishlist.")
        return redirect(f"{reverse('login')}?next={next_url}")
    product = get_object_or_404(Product, pk=pk)
    existing = Wishlist.objects.filter(user=request.user, product=product)
    if existing.exists():
        existing.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)
    return redirect(next_url)

def cart_add(request, pk):
    next_url = request.META.get("HTTP_REFERER") or reverse("home")
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to add items to your cart.")
        return redirect(f"{reverse('login')}?next={next_url}")
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
    return redirect("cart")

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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'quote'

    def perform_create(self, serializer):
        quote = serializer.save()
        subject = f"New Quote Request from {quote.name}"
        body = (
            f"Name: {quote.name}\n"
            f"Company: {quote.company_name or '-'}\n"
            f"Country: {quote.country or '-'}\n"
            f"Contact: {quote.contact_info}\n"
            f"Product Required: {quote.product_required or '-'}\n"
            f"Quantity: {quote.quantity or '-'}\n"
            f"Customization Requirements: {quote.customization_requirements or '-'}\n"
            f"Message: {quote.message or '-'}\n"
        )
        try:
            send_mail(
                subject,
                body,
                f"Leather Dynamic <{django_settings.EMAIL_HOST_USER}>",
                [django_settings.QUOTE_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass



