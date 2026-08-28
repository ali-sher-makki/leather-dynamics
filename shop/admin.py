from django.contrib import admin
from .models import Product, QuoteRequest, Category

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(QuoteRequest)
