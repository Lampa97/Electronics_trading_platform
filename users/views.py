from rest_framework import generics, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdmin
from .serializers import EmployeeStatusUpdateSerializer, UserSerializer, UserTokenObtainPairSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """API view to create a new user account."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.is_active = True
        user.save()


class EmployeeStatusUpdateAPIView(views.APIView):
    """API view to update the employee status of a user."""

    serializer_class = EmployeeStatusUpdateSerializer
    permission_classes = (IsAdmin,)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        email = request.data.get("email")

        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            else:
                user.is_employee = True
                user.save()
                return Response({"status": "Employee status updated successfully"})
        elif email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            else:
                user.is_employee = True
                user.save()
                return Response({"status": "Employee status updated successfully"})
        return Response({"error": "Please provide either user_id or email"}, status=400)


class UsersListAPIView(generics.ListAPIView):
    """API view to list all users. Only accessible by admin users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


class EmployeeListAPIView(generics.ListAPIView):
    """API view to list all employees. Only accessible by admin users."""

    queryset = User.objects.filter(is_employee=True)
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


class UserTokenObtainPairView(TokenObtainPairView):
    """Custom view to obtain JWT token with additional user information."""

    serializer_class = UserTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data["email"])
        user.save()
        return response
