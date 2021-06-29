from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .models import Note, Category
from .serializers import NoteSerializer
from .filters import NotesFilterSet


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = NotesFilterSet
    ordering_fields = ["date_updated", "category", "is_favorite"]
    ordering = ["date_updated"]


