#reports/views/view_reports_by_date.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.dateparse import parse_date
from django.utils.timezone import localdate

from reports.models.resident_report import ResidentReport


class ViewReportsByDateView(LoginRequiredMixin, TemplateView):
    template_name = "reports/view_reports_by_date.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        raw_date = self.request.GET.get("date")
        if raw_date:
            selected_date = parse_date(raw_date)  # ← parse_date ждёт строку, всё ок
        else:
            selected_date = localdate()
        context["selected_date"] = selected_date

        reports = ResidentReport.objects.filter(date=selected_date)\
            .select_related(
                "resident",
                "emotional_state",
                "physical_state",
                "motivation",
                "daily_dynamics",
                "mrp_activity",
                "family_activity"
            )\
            .prefetch_related(
                "positive_traits",
                "negative_traits",
                "task_comments__assigned_task",
                "role_statuses__role_assignment__role"
            )

        prepared_reports = []

        for report in reports:
            # 🔍 Комментарии по задачам
            task_comments = {
                tc.assigned_task.task.title: tc.comment
                for tc in report.task_comments.all()
            }

            # 👔 Статусы по функции
            role_statuses = {
                rs.role_assignment.role.name: rs.get_status_display()
                for rs in report.role_statuses.all()
            }

            prepared_reports.append({
                "resident": report.resident,
                "emotional_state": str(report.emotional_state) if report.emotional_state else "—",
                "physical_state": str(report.physical_state) if report.physical_state else "—",
                "motivation": str(report.motivation) if report.motivation else "—",
                "daily_dynamics": str(report.daily_dynamics) if report.daily_dynamics else "—",
                "mrp_activity": str(report.mrp_activity) if report.mrp_activity else "—",
                "family_activity": str(report.family_activity) if report.family_activity else "—",
                "positive_traits": ", ".join(t.name for t in report.positive_traits.all()) or "—",
                "negative_traits": ", ".join(t.name for t in report.negative_traits.all()) or "—",
                "usts_info_shared": "Да" if report.usts_info_shared else "Нет",
                "usts_format_followed": "Да" if report.usts_format_followed else "Нет",
                "usts_comment": report.usts_comment or "—",
                "comment": report.comment or "—",
                "task_comments": task_comments,
                "role_statuses": role_statuses,
            })

        context["reports"] = prepared_reports
        return context