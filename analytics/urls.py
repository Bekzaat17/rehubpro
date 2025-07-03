from django.urls import path
from analytics.views import analytics_main_view, analytics_full_page_view
from analytics.views.main import analytics_full_page_view

app_name = "analytics"

urlpatterns = [
    path("full/", analytics_main_view, name="analytics_full"),
    path("full/page/", analytics_full_page_view, name="analytics_full_page"),
]