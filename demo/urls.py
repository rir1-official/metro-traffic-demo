from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/mock-update/", views.mock_update, name="mock_update"),
]
