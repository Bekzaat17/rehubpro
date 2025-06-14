# reports/views/fill_all_reports_view.py

from django.views.generic import TemplateView
from django.utils import timezone

from residents.models import Resident
from reports.models.resident_report import ResidentReport
from reports.forms.resident_report_form import ResidentReportForm


class FillAllReportsView(TemplateView):
    template_name = "reports/fill_all_reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        active_residents = Resident.objects.filter(is_active=True)

        report_forms = []
        for resident in active_residents:
            report, _ = ResidentReport.objects.get_or_create(
                resident=resident,
                date=today,
                defaults={'created_by': self.request.user}
            )

            can_edit = report.date == today  # 💡 Editable только сегодня
            form = ResidentReportForm(
                resident=resident,
                date=today,
                initial={
                    "emotional_state": report.emotional_state_id,
                    "physical_state": report.physical_state_id,
                    "motivation": report.motivation_id,
                    "daily_dynamics": report.daily_dynamics_id,
                    "positive_traits": report.positive_traits.values_list("id", flat=True),
                    "negative_traits": report.negative_traits.values_list("id", flat=True),
                    "mrp_activity": report.mrp_activity_id,
                    "family_activity": report.family_activity_id,
                    "comment": report.comment,
                }
            )
            report_forms.append({
                "resident": resident,
                "form": form,
                "report_id": report.id,
                "is_filled": report.is_filled(),
                "can_edit": can_edit,
            })

        context["reports"] = report_forms
        return context