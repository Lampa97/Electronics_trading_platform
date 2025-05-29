from django.urls import path

from api.apps import ApiConfig
from . import views

app_name = ApiConfig.name

urlpatterns = [
    path("cells/", views.SalesNetworkCellListView.as_view(), name="cell-list"),
    path("cell/<int:pk>/", views.SalesNetworkCellDetailView.as_view(), name="cell-detail"),
    path("cell/create/", views.SalesNetworkCellCreateView.as_view(), name="cell-create"),
    path("cell/<int:pk>/update/", views.SalesNetworkCellUpdateView.as_view(), name="cell-update"),
    path("cell/<int:pk>/delete", views.SalesNetworkCellDestroyView.as_view(), name="cell-destroy"),

    path("contacts/", views.ContactListView.as_view(), name="contacts-list" ),
    path("contact/<int:pk>/", views.ContactDetailView.as_view(), name="contact-detail"),
    path("contact/create/", views.ContactCreateView.as_view(), name="contact-create"),
    path("contact/<int:pk>/update/", views.ContactUpdateView.as_view(), name="contact-update"),
    path("contact/<int:pk>/delete", views.ContactDeleteView.as_view(), name="contact-destroy"),

    path("products/", views.ProductListView.as_view(), name="products-list"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("product/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product-update"),
    path("product/<int:pk>/delete", views.ProductDeleteView.as_view(), name="product-destroy"),

]
