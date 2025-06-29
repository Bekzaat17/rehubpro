from django.urls import path
from analytics.views import analytics_main_view

urlpatterns = [
    path("full/", analytics_main_view, name="analytics_full"),
]