from rest_framework import serializers
from .models import Product, QuoteRequest, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "image"]

    def get_category(self, obj):
        return obj.category.name if obj.category else None

class QuoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = ["id", "name", "company_name", "country", "contact_info", "product_required", "quantity", "customization_requirements", "message"]
