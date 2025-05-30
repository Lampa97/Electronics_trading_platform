from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Contact, Product, SalesNetworkCell
from users.models import User


class APITests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create(
            email="admin@mail.com", password="adminpassword", is_staff=True, is_superuser=True, is_employee=True
        )
        self.client.login(email="admin@mail.com", password="adminpassword")

        self.contact = Contact.objects.create(
            email="doe@mail.com", country="USA", city="New York", street="123 Main St", house_number="1A"
        )
        self.product = Product.objects.create(name="Product A", model="X", release_date="2025-01-01")
        self.sales_network_cell = SalesNetworkCell.objects.create(
            name="My Factory", hierarchy_name="Factory", debt=1000.00
        )

    def test_list_contacts(self):
        url = reverse("api:contact-list")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact(self):
        url = reverse("api:contact-create")
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "email": "jane@mail.com",
            "country": "Canada",
            "city": "Ottawa",
            "street": "123 Sec St",
            "house_number": "5A",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Contact.objects.filter(email="jane@mail.com").exists())

    def test_retrieve_contact(self):
        url = reverse("api:contact-detail", args=[self.contact.id])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.contact.email)

    def test_update_contact(self):
        url = reverse("api:contact-update", args=[self.contact.id])
        data = {"email": "update@mail.com"}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.email, "update@mail.com")

    def test_delete_contact(self):
        url = reverse("api:contact-destroy", args=[self.contact.id])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    def test_list_products(self):
        url = reverse("api:product-list")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        url = reverse("api:product-create")
        data = {"name": "Product B", "model": "Y", "release_date": "2024-01-01"}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="Product B").exists())

    def test_retrieve_product(self):
        url = reverse("api:product-detail", args=[self.product.id])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_update_product(self):
        url = reverse("api:product-update", args=[self.product.id])
        data = {"name": "Individual Entrepreneur"}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Individual Entrepreneur")

    def test_delete_product(self):
        url = reverse("api:product-destroy", args=[self.product.id])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_list_sales_network_cells(self):
        url = reverse("api:cell-list")
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sales_network_cell(self):
        url = reverse("api:cell-create")
        data = {"name": "My Retail", "hierarchy_name": "Retail Network", "debt": 500.00}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SalesNetworkCell.objects.filter(name="My Retail").exists())

    def test_retrieve_sales_network_cell(self):
        url = reverse("api:cell-detail", args=[self.sales_network_cell.id])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "My Factory")

    def test_update_contact_sales_network_cell(self):
        url = reverse("api:cell-update", args=[self.sales_network_cell.id])
        data = {"contact": self.contact.id}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_sales_network_cell(self):
        url = reverse("api:cell-update", args=[self.sales_network_cell.id])
        data = {"product": self.product.id}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hierarchy_levels_sales_network_cell(self):
        url = reverse("api:cell-create")
        data = {
            "name": "My Factory2",
            "hierarchy_name": "Factory",
            "debt": 500.00,
            "supplier": self.sales_network_cell.id,
        }
        self.client.force_authenticate(user=self.admin_user)
        with self.assertRaises(ValidationError):
            self.client.post(url, data)

    def test_hierarchy_level_change_network_cell(self):
        url = reverse("api:cell-create")
        data = {
            "name": "Individual Entrepreneur1",
            "hierarchy_name": "Individual Entrepreneur",
            "debt": 500.00,
            "supplier": self.sales_network_cell.id,
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_cell = SalesNetworkCell.objects.get(name="Individual Entrepreneur1")
        self.assertEqual(created_cell.hierarchy_level, 1)
        self.assertTrue(SalesNetworkCell.objects.filter(name="Individual Entrepreneur1").exists())

    def test_delete_sales_network_cell(self):
        url = reverse("api:cell-destroy", args=[self.sales_network_cell.id])
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SalesNetworkCell.objects.filter(id=self.sales_network_cell.id).exists())

    def test_update_sales_network_cell_debt_field(self):
        url = reverse("api:cell-update", args=[self.sales_network_cell.id])
        data = {"debt": 2000.00}
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("debt", response.data)
        self.assertEqual(response.data["debt"], "This field can be updated only in admin panel.")

    def test_update_sales_network_cell_invalid_contact_field(self):
        url = reverse("api:cell-update", args=[self.sales_network_cell.id])
        data = {"contact": 9999}  # Invalid contact ID
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("contact", response.data)
        self.assertEqual(response.data["contact"], "Invalid contact ID.")

    def test_update_sales_network_cell_invalid_products_field(self):
        url = reverse("api:cell-update", args=[self.sales_network_cell.id])
        data = {"products": [9]}  # Invalid product ID
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("products", response.data)
        self.assertEqual(str(response.data["products"]), "Invalid product IDs: 9")
