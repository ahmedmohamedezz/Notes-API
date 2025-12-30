from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from notes.models import Note
from notes.serializers import NotesSerializer


# Create your views here.
def index(request):
    return JsonResponse({"message": "Welcome to Notes API"})


# 3. ViewSets (actions instead of HTTP methods of APIView)
class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer
    permission_classes = [AllowAny]
