from django.urls import path
from .views import license_expired_view

app_name = "licenses"

urlpatterns = [
    path("expired/", license_expired_view, name="license_expired"),
]