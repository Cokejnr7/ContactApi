from django.test import SimpleTestCase
from django.urls import resolve, reverse
from .views import ContactListCreateView, ContactDetailView
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

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
    def setUp(self):
        user_details = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "firstname": "test",
            "lastname": "user",
            "password": "12345",
        }
        self.user = User.objects.create(**user_details)

        self.client.force_authenticate(user=self.user)

    def test_create_contact(self):
        pass
