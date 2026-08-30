from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .forms import LoginForm

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop_categories, name="shop-list"),
    path("shop/all/", views.shop_all_products, name="shop-all"),
    path("shop/category/<int:pk>/", views.shop_category_products, name="shop-category"),
    path("shop/<int:pk>/", views.product_detail, name="product-page"),
    path("contact/", views.contact_page, name="contact-page"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("api/", include(router.urls)),
    path("api/quote/", views.QuoteRequestCreateView.as_view(), name="quote-create"),
]
