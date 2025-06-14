# reports/urls.py

from django.urls import path
from .views.fill_all_reports_view import FillAllReportsView
from .views.save_report_view import SaveReportView

app_name = "reports"

urlpatterns = [
    path("fill/", FillAllReportsView.as_view(), name="fill_reports"),
    path("save/<int:report_id>/", SaveReportView.as_view(), name="save_report"),
]