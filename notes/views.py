from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from notes.models import Note
from notes.serializers import NotesSerializer


# Create your views here.
def index(request):
    return JsonResponse({"message": "Hello, world!"})


@api_view(["GET", "POST"])
def notes_view(request):
    if request.method == "GET":
        notes = Note.objects.all()
        return Response(NotesSerializer(notes, many=True).data)
    else:
        serializer = NotesSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
