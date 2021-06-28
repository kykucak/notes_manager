from rest_framework import serializers

from .models import Note, Category


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
