from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .serializers import ContactSerializer, ProductSerializer, SalesNetworkCellSerializer
from .paginators import CustomPagination
from .models import Contact, Product, SalesNetworkCell

class ContactListView(generics.ListAPIView):
    """View to list contacts.
    Allows filtering by country."""
    serializer_class = ContactSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]

    def get_queryset(self):
        return Contact.objects.all()

class ContactCreateView(generics.CreateAPIView):
    """View to create contacts."""
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveUAPIView):
    """View to retrieve a specific contact."""
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.all()

class ContactUpdateView(generics.UpdateAPIView):
    """View to update a specific contact."""
    serializer_class = ContactSerializer

class ContactDeleteView(generics.DestroyAPIView):
    """View to delete a specific contact."""
    serializer_class = ContactSerializer


class ProductListView(generics.ListAPIView):
    """View to list products."""
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Product.objects.all()

class ProductCreateView(generics.CreateAPIView):
    """View to create products."""
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    """View to retrieve a specific product."""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

class ProductUpdateView(generics.UpdateAPIView):
    """View to update a specific product."""
    serializer_class = ProductSerializer

class ProductDeleteView(generics.DestroyAPIView):
    """View to delete a specific product."""
    serializer_class = ProductSerializer


class SalesNetworkCellListView(generics.ListAPIView):
    """View to list sales network cells.
    Allows filtering by contact's country."""
    serializer_class = SalesNetworkCellSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["contact__country"]

    def get_queryset(self):
        return SalesNetworkCell.objects.all()

class SalesNetworkCellCreateView(generics.CreateAPIView):
    """View to create sales network cells."""
    serializer_class = SalesNetworkCellSerializer


class SalesNetworkCellDetailView(generics.RetrieveAPIView):
    """View to retrieve  a specific sales network cell."""
    serializer_class = SalesNetworkCellSerializer

    def get_queryset(self):
        return SalesNetworkCell.objects.all()

class SalesNetworkCellDestroyView(generics.DestroyAPIView):
    """View to delete a specific sales network cell."""
    serializer_class = SalesNetworkCellSerializer


class SalesNetworkCellUpdateView(generics.UpdateAPIView):
    """View to update a specific sales network cell."""
    serializer_class = SalesNetworkCellSerializer

    def get_queryset(self):
        return SalesNetworkCell.objects.all()

    def update(self, request, *args, **kwargs):
        """Override the update method to prevent updating the 'debt' field via put or patch request."""
        if "debt" in request.data:
            raise ValidationError({"debt": "This field can be updated only in admin panel."})
        return super().update(request, *args, **kwargs)