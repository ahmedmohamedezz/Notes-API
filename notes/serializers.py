from rest_framework import serializers
from notes.models import Note


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Title is required.",
            "blank": "Title cannot be empty.",
            "invalid": "Title must be a string.",
        },
    )

    content = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Content is required.",
            "blank": "Content cannot be empty.",
        },
    )

    class Meta:
        model = Note
        fields = "__all__"

    def validate_title(self, value):
        if len(value) > 255:
            raise serializers.ValidationError("Title can't exceed 255 characters.")

        return value
