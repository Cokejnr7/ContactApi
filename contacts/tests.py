from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .views import ContactListCreateView, ContactDetailView
import jwt


# Create your tests here.

User = get_user_model()


class TestUrls(SimpleTestCase):
    def test_contacts_list_create_url(self):
        url = reverse("contacts")
        self.assertEqual(resolve(url).func.view_class, ContactListCreateView)

    def tests_contacts_detail_url(self):
        url = reverse("contact", kwargs={"id": 1})
        self.assertEqual(resolve(url).func.view_class, ContactDetailView)


class TestContactListCreateView(APITestCase):
    contacts_url = reverse("contacts")

    def setUp(self):
        user_details = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "12345",
        }
        self.user = User.objects.create(**user_details)
        self.token = jwt.encode(
            {"username": self.user.username},
            settings.JWT_SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_contacts_authenticated(self):
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contacts_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
