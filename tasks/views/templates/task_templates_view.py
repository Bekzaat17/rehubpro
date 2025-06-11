from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from tasks.models.task_template import TaskTemplate
from django.shortcuts import get_object_or_404

import json

class TaskTemplatesView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_templates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_templates'] = TaskTemplate.objects.all()
        return context


@method_decorator(ensure_csrf_cookie, name='dispatch')
class TaskTemplateAPI(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        template_id = data.get('id')
        title = data.get('title', '')
        description = data.get('description', '')
        task_type = data.get('task_type', 'short_term')

        if template_id:
            template = TaskTemplate.objects.get(id=template_id)
            template.title = title
            template.description = description
            template.task_type = task_type
            template.save()
        else:
            template = TaskTemplate.objects.create(
                title=title,
                description=description,
                task_type=task_type
            )

        return JsonResponse({
            'id': template.id,
            'title': template.title,
            'description': template.description,
            'task_type': template.task_type,
        })

    def get(self, request):
        templates = TaskTemplate.objects.all().values('id', 'title', 'description', 'task_type')
        return JsonResponse(list(templates), safe=False)

    def delete(self, request, *args, **kwargs):
        """
        Удаляет шаблон по ID, переданному в URL.
        """
        template_id = kwargs.get('template_id')
        template = get_object_or_404(TaskTemplate, id=template_id)
        template.delete()
        return JsonResponse({'status': 'deleted'})