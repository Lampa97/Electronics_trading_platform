from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Product, SalesNetworkCell


@admin.register(SalesNetworkCell)
class SalesNetworkCellAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "hierarchy_name",
        "hierarchy_level",
        "supplier_link",
        "contact",
        "products_list",
        "debt",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = (
        "contact__city",
        "hierarchy_level",
    )
    ordering = (
        "hierarchy_level",
        "-created_at",
    )
    actions = ["clear_debt"]
    exclude = ("hierarchy_level",)

    def supplier_link(self, obj):
        """Adding a link to the supplier in the admin interface."""
        if obj.supplier:
            return format_html(
                '<a href="/admin/api/salesnetworkcell/{}/change/">{}</a>', obj.supplier.id, obj.supplier.name
            )
        return "-"

    supplier_link.short_description = "Supplier"

    def products_list(self, obj):
        """Showing a list of products in the admin interface."""
        return ", ".join([product.name for product in obj.products.all()])

    products_list.short_description = "Products"

    def clear_debt(self, request, queryset):
        """Admin action for clearing debt"""
        queryset.update(debt=0)
        self.message_user(request, "Debt successfully cleared")

    clear_debt.short_description = "Clear the debt for selected cells"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "country",
        "city",
        "street",
        "house_number",
    )
    search_fields = ("country", "city", "street", "house_number")
    list_filter = ("country", "city")
    ordering = ("country", "city", "street", "house_number")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "model",
        "release_date",
    )
    search_fields = ("name", "model", "release_date")
    list_filter = ("release_date",)
    ordering = ("-release_date",)
