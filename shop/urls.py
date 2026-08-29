from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop_categories, name="shop-list"),
    path("shop/all/", views.shop_all_products, name="shop-all"),
    path("shop/category/<int:pk>/", views.shop_category_products, name="shop-category"),
    path("shop/<int:pk>/", views.product_detail, name="product-page"),
    path("contact/", views.contact_page, name="contact-page"),
    path("api/", include(router.urls)),
    path("api/quote/", views.QuoteRequestCreateView.as_view(), name="quote-create"),
]
