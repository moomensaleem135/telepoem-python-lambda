from .views import IndexView
from django.urls import path

urlpatterns = [
    path("upload_file", IndexView.as_view(), name="index"),
]
