# analytics/views/main.py
from django.http import JsonResponse
from django.shortcuts import render

from analytics.metrics.daily_dynamics import DailyDynamicsMetric
from analytics.metrics.family_activity import FamilyActivityMetric
from analytics.metrics.motivation import MotivationMetric
from analytics.metrics.mrp_activity import MRPActivityMetric
from analytics.metrics.negative_traits import NegativeTraitsMetric
from analytics.metrics.physical_state import PhysicalStateMetric
from analytics.metrics.positive_traits import PositiveTraitsMetric
from analytics.metrics.emotional_state import EmotionalStateMetric
from analytics.metrics.resident_role_responsibility import ResidentRoleResponsibilityMetric
from analytics.metrics.task_progress_timeline import TaskProgressTimelineMetric
from analytics.metrics.usts_format_followed import USTSFormatFollowedMetric
from analytics.metrics.usts_info_shared import USTSInfoSharedMetric
from reports.models import ResidentReport

from analytics.director import ReportDirector
from residents.models import Resident


def analytics_main_view(request):
    queryset = ResidentReport.objects.all()
    filters = request.GET.dict()

    director = ReportDirector(
        queryset=queryset,
        filters=filters,
        metric_classes=[
            EmotionalStateMetric,
            PhysicalStateMetric,
            MotivationMetric,
            DailyDynamicsMetric,
            PositiveTraitsMetric,
            NegativeTraitsMetric,
            MRPActivityMetric,
            FamilyActivityMetric,
            USTSInfoSharedMetric,
            USTSFormatFollowedMetric,
            TaskProgressTimelineMetric,
            ResidentRoleResponsibilityMetric
            # ...
        ]
    )

    result = director.run()
    return JsonResponse(result)

def analytics_full_page_view(request):
    residents = Resident.objects.all()
    return render(request, "analytics/full_page.html", {
        "residents": residents
    })