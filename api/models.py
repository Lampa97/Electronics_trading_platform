from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError

class SalesNetworkCell(models.Model):
    """Model representing a cell in the sales network hierarchy."""
    LEVEL_CHOICES = [
        ("Factory", "Factory"),
        ("Retail Network", "Retail Network"),
        ("Individual Entrepreneur", "Individual Entrepreneur"),
    ]


    name = models.CharField(max_length=100, verbose_name="Cell Name")
    hierarchy_level = models.PositiveIntegerField(
        verbose_name="Hierarchy Level", validators=[MinValueValidator(0), MaxValueValidator(2)])
    hierarchy_name = models.CharField(max_length=100, choices=LEVEL_CHOICES, verbose_name="Hierarchy Name", blank=True)
    contact = models.OneToOneField("Contact", on_delete=models.CASCADE, verbose_name="Contact Information", null=True, blank=True)
    products = models.ManyToManyField("Product", blank=True, null=True, verbose_name="Products")
    supplier = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Supplier")
    debt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Debt", default=0.00)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def save(self, *args, **kwargs):
        """Override save method to ensure hierarchy level and supplier are set correctly"""
        level_names = {"Factory": 0, "Retail Network": 1, "Individual Entrepreneur": 2}
        self.hierarchy_level = level_names.get(self.hierarchy_name)

        if self.supplier and self.hierarchy_level == self.supplier.hierarchy_level:
            raise ValidationError("Hierarchy level cannot be the same as the supplier")

        if self.hierarchy_level == 0:  # Factory level
            self.supplier = None
        elif self.hierarchy_level == 2 and self.supplier and self.supplier.hierarchy_level == 0:
            self.hierarchy_level = 1

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sales Network Cell"
        verbose_name_plural = "Sales Network Cells"
        ordering = ["hierarchy_level", "name"]

    def __str__(self):
        return f"{self.name} (Level {self.hierarchy_level})"


class Contact(models.Model):
    """Model representing contact information for a sales network cell."""
    email = models.EmailField(max_length=254, verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Country")
    city = models.CharField(max_length=100, verbose_name="City")
    street = models.CharField(max_length=100, verbose_name="Street")
    house_number = models.CharField(max_length=10, verbose_name="House Number")

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["email"]

    def __str__(self):
        return f"{self.email} - {self.city}, {self.street} {self.house_number}"

class Product(models.Model):
    """Model representing a product in the sales network."""
    name = models.CharField(max_length=100, verbose_name="Product Name")
    model = models.CharField(max_length=100, verbose_name="Model", null=True, blank=True)
    release_date = models.DateField(verbose_name="Release Date", null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.model}"
