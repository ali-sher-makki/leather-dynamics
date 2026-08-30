from django.contrib import admin
from .models import Product, QuoteRequest, Category, Profile, Wishlist, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ["id", "user", "full_name", "status", "total_amount", "created_at"]
    list_filter = ["status"]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(QuoteRequest)
admin.site.register(Profile)
admin.site.register(Wishlist)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
