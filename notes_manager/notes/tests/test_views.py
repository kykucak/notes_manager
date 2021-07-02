from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from datetime import datetime, timedelta

from ..models import Note, Category


class NotesTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("note-list")
        user = User.objects.create_user(
            username="test_name",
            password="testing321"
        )
        cls.category_1 = Category.objects.create(name="Test")
        cls.category_2 = Category.objects.create(name="Todo")
        cls.note_1 = Note.objects.create(
            title="Learn DRF",
            content="some content laalalal",
            category=cls.category_1,
            author=user,
        )
        cls.note_2 = Note.objects.create(
            title="Play guitar",
            content="some content laalalal",
            category=cls.category_2,
            author=user,
            is_favorite=True
        )

    @staticmethod
    def get_date(days_delta: int = 0):
        """Returns date now + days_delta in  %Y-%m-%d format"""
        if not isinstance(days_delta, int) or isinstance(days_delta, bool):
            raise TypeError

        date = datetime.now() + timedelta(days=days_delta)

        return date.strftime("%Y-%m-%d")

    def test_right_notes_when_no_query_params(self):
        """"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Play guitar")
        self.assertEqual(response.data[-1].get("title"), "Learn DRF")

    def test_right_note_when_right_category_name(self):
        """Checks if note with an appropriate category name is returned"""
        data = {"category": "Todo"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Play guitar")
        self.assertEqual(response.data[0].get("category"), 2)  # Needed category id equals to 1

    def test_empty_list_when_wrong_category_name(self):
        """Checks if empty list is returned, when invalid category name is passed"""
        data = {"category": "Something"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_right_note_when_true_isFavorite(self):
        """Checks if note with is_favorite=True is returned"""
        data = {"is_favorite": "true"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Play guitar")

    def test_right_note_when_false_isFavorite(self):
        """Checks if note with is_favorite=False is returned"""
        data = {"is_favorite": "false"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")

    def test_right_note_when_icontains_title(self):
        """
        Checks if note with title, that contains "learn" is returned
        """
        data = {"title": "learn"}  # reference to "Learn DRF"
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")

    def test_right_note_when_iexact_title(self):
        """
        Checks if note with title="Play guitar" is returned
        """
        data = {"title": "Play guitar"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get("title"), "Play guitar")

    def test_empty_list_when_wrong_title(self):
        """
        Checks if empty list is returned,
        when invalid title was passed
        """
        data = {"title": "WOOD"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_right_note_when_right_dateBefore(self):
        """
        Checks if notes in passed date range is returned
        """
        date = self.get_date(days_delta=1)  # now + 1 day
        data = {"date_before": date}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")
        self.assertEqual(response.data[1].get("title"), "Play guitar")

    def test_empty_list_when_wrong_dateBefore(self):
        """
        Checks if empty list is returned,
        when there is no notes with passed date_before
        """
        date = self.get_date(days_delta=-1)  # now - 1 day
        data = {"date_before": date}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_400_when_invalid_dateBefore(self):
        """
        Checks if 400 Bad Request is sent,
        when client send invalid date_before
        """
        data = {"date_before": "02-07-21"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("date")[0], "Enter a valid date/time.")

    def test_right_note_when_right_dateAfter(self):
        """
        Checks if notes in passed date range is returned
        """
        date = self.get_date()  # now
        data = {"date_after": date}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")
        self.assertEqual(response.data[1].get("title"), "Play guitar")

    def test_empty_list_when_wrong_dateAfter(self):
        """
        Checks if empty list is returned,
        when there is no notes with passed date_after
        """
        date = self.get_date(days_delta=1)  # now + 1 day
        data = {"date_after": date}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_400_when_invalid_dateAfter(self):
        """
        Checks if 400 Bad Request is sent,
        when client send invalid date_after
        """
        data = {"date_after": "02-07-21"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("date")[0], "Enter a valid date/time.")

    def test_right_order_when_asc_dateUpdated(self):
        """
        Checks if notes are returned in right order,
        when order=date_update is passed
        """
        data = {"order": "date_update"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")
        self.assertEqual(response.data[-1].get("title"), "Play guitar")

    def test_right_order_when_desc_dateUpdate(self):
        """
        Checks if notes are returned in right order,
        when order=-date_update is passed
        """
        data = {"order": "-date_update"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")
        self.assertEqual(response.data[-1].get("title"), "Play guitar")

    def test_right_order_when_asc_category(self):
        """"""
        data = {"order": "Todo"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("category"), self.category_1.id)
        self.assertEqual(response.data[-1].get("category"), self.category_2.id)

    def test_right_order_when_asc_isFavorite(self):
        """"""
        data = {"order": "is_favorite"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Learn DRF")
        self.assertEqual(response.data[-1].get("title"), "Play guitar")

    def test_right_order_when_desc_isFavorite(self):
        """"""
        data = {"order": "-is_favorite"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("title"), "Play guitar")
        self.assertEqual(response.data[-1].get("title"), "Learn DRF")
