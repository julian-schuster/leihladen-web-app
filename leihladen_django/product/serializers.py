from rest_framework import serializers

from .models import Category, Product, Wishlist

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "get_image",
            "get_images",
            "get_category_names",
            "quantity",
            "available",
            "categories",
            "date_added",
            "dimension",
            "fee",
            "deposit",
            "weight",
            "smallPieces"
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products"
        )

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = (
            "id",
            "qr_code_text",
            "client_id",
            "date_added",
        )