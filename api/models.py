from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SalesNetworkCell(models.Model):
    LEVEL_CHOICES = [
        (0, "Factory"),
        (1, "Retail Network"),
        (2, "Individual Entrepreneur"),
    ]

    name = models.CharField(max_length=100, verbose_name="Cell Name")
    hierarchy_level = models.PositiveIntegerField(
        verbose_name="Hierarchy Level",
        choices=LEVEL_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )
    supplier = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Supplier"
    )
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Debt", default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def save(self, *args, **kwargs):
        """ Override save method to ensure hierarchy level and supplier are set correctly """
        if self.hierarchy_level == 0:  # Factory level
            self.supplier = None
        if self.supplier and self.supplier.hierarchy_level == 0: # If supplier is a factory, set hierarchy level to 1
            self.hierarchy_level = 1
        super().save(*args, **kwargs)

class Contact(models.Model):
    email = models.EmailField(max_length=254, verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Country")
    city = models.CharField(max_length=100, verbose_name="City")
    street = models.CharField(max_length=100, verbose_name="Street")
    street_number = models.CharField(max_length=10, verbose_name="Street Number")


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    model = models.CharField(max_length=100, verbose_name="Model", null=True, blank=True)
    release_date = models.DateField(verbose_name="Release Date", null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.model}