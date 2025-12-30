from django.urls import path, include

from rest_framework.routers import DefaultRouter

from notes import views

router = DefaultRouter()
router.register(r"notes", views.NotesViewSet, basename="note")

urlpatterns = [path("", views.index, name="index_view"), path("", include(router.urls))]
