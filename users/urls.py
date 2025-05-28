from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig

from .views import (
    EmployeeListAPIView,
    EmployeeStatusUpdateAPIView,
    UserCreateAPIView,
    UsersListAPIView,
    UserTokenObtainPairView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", UserTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("employees/", EmployeeListAPIView.as_view(), name="employees_list"),
    path("", UsersListAPIView.as_view(), name="users_list"),
    path("employee/status/update/", EmployeeStatusUpdateAPIView.as_view(), name="employee_status_update"),
]
