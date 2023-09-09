from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
import jwt
from .views import ContactListCreateView, ContactDetailView
from .serializers import ContactSerializer


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
        self.serializer_class = ContactSerializer
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

    def test_list_contacts_authenticated(self):
        serializer = self.serializer_class()
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(
        #     response.data,
        # )

    def test_list_contacts_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.contacts_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_contact_authenticated(self):
        data = {
            "owner": self.user,
            "country_code": "+234",
            "first_name": "test",
            "last_name": "contact1",
            "phone_number": "8736767278",
        }
        serializer = self.serializer_class(data=data)

        self.assertEqual(serializer.is_valid(), True)
        response = self.client.post(self.contacts_url, serializer.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], data["first_name"])


class TestCustomerDetailView(APITestCase):
    pass
