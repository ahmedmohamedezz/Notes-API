from django.urls import path
from notes import views

urlpatterns = [path("", views.index, name="index_view")]
