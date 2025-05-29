from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@mail.com",
            "password": "testpassword",
        }
        self.admin_user = User.objects.create(
            email="admin@mail.com", password="adminpassword", is_staff=True, is_superuser=True, is_employee=True
        )
        self.client.login(email="admin@mail.com", password="adminpassword")

    def test_create_user(self):
        url = reverse("users:register")
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_change_employee_status(self):
        user = User.objects.create(**self.user_data)
        url = reverse("users:employee_status_update")
        self.client.force_authenticate(user=self.admin_user)
        data = {"email": user.email}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_employee)

    def test_change_employee_status_invalid_user_email(self):
        url = reverse("users:employee_status_update")
        self.client.force_authenticate(user=self.admin_user)
        data = {"email": "invalid@mail.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_employee_status_invalid_user_id(self):
        url = reverse("users:employee_status_update")
        self.client.force_authenticate(user=self.admin_user)
        data = {"user_id": 9}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
