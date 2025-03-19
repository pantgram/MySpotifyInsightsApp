from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_recent, name="get_recent"),
]