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
    path("contacts/", views.Co)

]
