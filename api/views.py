from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .serializers import ContactSerializer, ProductSerializer, SalesNetworkCellSerializer
from .paginators import CustomPagination
from .models import Contact, Product, SalesNetworkCell

class ContactListCreateView(generics.ListCreateAPIView):
    """View to list and create contacts.
    Allows filtering by country."""
    serializer_class = ContactSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]

    def get_queryset(self):
        return Contact.objects.all()


class ContactDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a specific contact."""
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.all()


class ProductListCreateView(generics.ListCreateAPIView):
    """View to list and create products."""
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a specific product."""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class SalesNetworkCellListCreateView(generics.ListCreateAPIView):
    """View to list and create sales network cells.
    Allows filtering by contact's country."""
    serializer_class = SalesNetworkCellSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["contact__country"]

    def get_queryset(self):
        return SalesNetworkCell.objects.all()


class SalesNetworkCellDetailDeleteView(generics.RetrieveDestroyAPIView):
    """View to retrieve or delete a specific sales network cell."""
    serializer_class = SalesNetworkCellSerializer

    def get_queryset(self):
        return SalesNetworkCell.objects.all()


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