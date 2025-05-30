from rest_framework import serializers

from .models import Contact, Product, SalesNetworkCell


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""

    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    class Meta:
        model = Product
        fields = "__all__"


class SalesNetworkCellSerializer(serializers.ModelSerializer):
    """Serializer for SalesNetworkCell model."""

    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SalesNetworkCell
        fields = "__all__"
        read_only_fields = ("created_at", "hierarchy_level", "contact", "products")
