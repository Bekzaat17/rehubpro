from collections import defaultdict
from .base import BaseMetric
from analytics.charts.timeline import TimelineBuilder
from tasks.models.task_progress import TaskProgress

class TaskProgressTimelineMetric(BaseMetric):
    """
    Хронология активности заданий (по TaskProgress) на основе отфильтрованного queryset.
    Предполагается, что ReportDirector передал сюда TaskProgress queryset.
    """

    def calculate(self):
        timeline = defaultdict(list)

        for entry in self.queryset.select_related("assigned_task__task"):
            task = entry.assigned_task.task
            date_str = entry.created_at.date().isoformat()
            timeline[date_str].append({
                "task_title": task.title,
                "task_type": task.task_type,
                "stage": entry.get_stage_display(),
                "comment": entry.comment,
            })

        return {
            "title": "Хронология заданий",
            "timeline": dict(sorted(timeline.items()))
        }

    def get_chart_builder_class(self):
        return TimelineBuilder

    @classmethod
    def get_base_queryset(cls, filters):
        from tasks.models.task_progress import TaskProgress
        return TaskProgress.objects.all()

    @classmethod
    def get_filter_field(cls):
        return "created_at"  # Для TaskProgress