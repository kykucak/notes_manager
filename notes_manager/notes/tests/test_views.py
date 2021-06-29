from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Note, Category


class NoteFilteringTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("note-list")
        user = User.objects.create_user(
            username="test_name",
            password="testing321"
        )
        category_1 = Category.objects.create(name="Test")
        category_2 = Category.objects.create(name="Test2")
        note_1 = Note.objects.create(
            title="Learn DRF",
            content="some content laalalal",
            category=category_1,
            author=user,
        )
        note_1 = Note.objects.create(
            title="Play guitar",
            content="some content laalalal",
            category=category_2,
            author=user,
            is_favorite=True
        )

    def test_valid_category(self):
        """Checks if right notes were returned, when valid category name was passed"""
        data = {"category__name": "Test"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")
        self.assertEqual(response.data[0].get("category"), 1)  # Needed category id equals to 1

    def test_invalid_category(self):
        """Checks if empty list was returned, when invalid category name was passed"""
        data = {"category__name": "Something"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_true_favorite(self):
        """Checks if right notes were returned, when is_favorite=True was passed"""
        data = {"is_favorite": "true"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Play guitar")

    def test_false_favorite(self):
        """Checks if right notes were returned, when is_favorite=False was passed"""
        data = {"is_favorite": "false"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")

