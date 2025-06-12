# tasks/views/resident_tasks_view.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from residents.models import Resident
from tasks.models.assigned_task import AssignedTask



class ResidentTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/resident_tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Загружаем всех резидентов с их последним назначенным заданием
        residents = Resident.objects.all()

        resident_data = []
        for resident in residents:
            latest_task = (
                AssignedTask.objects
                .filter(resident=resident)
                .order_by('-assigned_at')
                .first()
            )
            resident_data.append({
                'resident': resident,
                'latest_task': latest_task
            })

        context['resident_data'] = resident_data
        return context