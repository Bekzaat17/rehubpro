# test/urls.py

from django.urls import path
from test.views.dev_panel_view import DevPanelView

app_name = 'test'

urlpatterns = [
    path("", DevPanelView.as_view(), name="dev_panel"),
]