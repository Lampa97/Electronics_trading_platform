from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating user accounts."""

    class Meta:
        model = User
        fields = ["id", "email", "is_employee"]


class EmployeeStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating employee status of a user."""

    class Meta:
        model = User
        fields = ["id", "email", "is_employee"]

    def validate(self, data):
        if not data.get("id") and not data.get("email"):
            raise serializers.ValidationError("Either 'id' or 'email' must be provided.")
        return data


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer for obtaining JWT token with additional user information."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["password"] = user.password

        return token
