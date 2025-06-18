# reports/urls.py

from django.urls import path
from .views.fill_all_reports_view import FillAllReportsView
from .views.save_report_view import SaveReportView
from .views.view_reports_by_date import ViewReportsByDateView

app_name = "reports"

urlpatterns = [
    path("fill/", FillAllReportsView.as_view(), name="fill_reports"),
    path("save/<int:report_id>/", SaveReportView.as_view(), name="save_report"),
    path("date/<date>/", ViewReportsByDateView.as_view(), name="view_by_date"),
]