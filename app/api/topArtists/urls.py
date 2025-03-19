from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:range>/",views.in_time_range,name="in_time_range")
]