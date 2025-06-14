from django import forms

from references.models import (
    EmotionalState, PhysicalState, Motivation, DailyDynamics,
    MrpActivity, FamilyActivity, CharacterTrait
)


class ResidentReportForm(forms.Form):
    """
    Форма для создания ежедневного отчёта по резиденту.
    НЕ ModelForm, так как добавляем кастомную динамику по задачам и ролям.
    """

    emotional_state = forms.ModelChoiceField(queryset=EmotionalState.objects.all())
    physical_state = forms.ModelChoiceField(queryset=PhysicalState.objects.all())
    motivation = forms.ModelChoiceField(queryset=Motivation.objects.all())
    daily_dynamics = forms.ModelChoiceField(queryset=DailyDynamics.objects.all())

    positive_traits = forms.ModelMultipleChoiceField(
        queryset=CharacterTrait.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    negative_traits = forms.ModelMultipleChoiceField(
        queryset=CharacterTrait.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    mrp_activity = forms.ModelChoiceField(queryset=MrpActivity.objects.all(), required=False)
    family_activity = forms.ModelChoiceField(queryset=FamilyActivity.objects.all(), required=False)

    comment = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, resident=None, date=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.resident = resident
        self.date = date
        self.task_comments = {}      # {task_id: comment}
        self.role_statuses = {}      # {role_id: status}
        self._init_dynamic_fields()

    def _init_dynamic_fields(self):
        """
        Подгружает активные задачи и роли — создаёт поля по ним.
        """
        from tasks.models.assigned_task import AssignedTask
        from tasks.models.task_progress import TaskProgress
        from roles.models.resident_role_assignment import ResidentRoleAssignment

        # Задачи (комментарии к ним)
        active_tasks = AssignedTask.objects.filter(
            resident=self.resident,
            status__in=["writing", "submitting"]
        )
        for task in active_tasks:
            field_name = f"task_comment_{task.id}"
            self.fields[field_name] = forms.CharField(
                label=f"Комментарий к задаче: {task.task.title}",
                required=False,
                widget=forms.Textarea(attrs={"rows": 2})
            )

        # Роли (оценка ответственности)
        roles = ResidentRoleAssignment.objects.filter(
            resident=self.resident,
            assigned_at__lte=self.date
        ).filter(
            unassigned_at__isnull=True
        ) | ResidentRoleAssignment.objects.filter(
            resident=self.resident,
            assigned_at__lte=self.date,
            unassigned_at__gte=self.date
        )

        for role in roles:
            field_name = f"role_status_{role.id}"
            self.fields[field_name] = forms.ChoiceField(
                label=f"Роль: {role.role.name}",
                choices=[
                    ("responsible", "Ответственный"),
                    ("irresponsible", "Безответственный")
                ],
                widget=forms.RadioSelect
            )

    def clean(self):
        cleaned_data = super().clean()

        # Собираем task_comments
        for name, value in self.cleaned_data.items():
            if name.startswith("task_comment_") and value.strip():
                task_id = int(name.split("_")[-1])
                self.task_comments[task_id] = value.strip()

        # Собираем role_statuses
        for name, value in self.cleaned_data.items():
            if name.startswith("role_status_"):
                role_id = name.split("_")[-1]
                self.role_statuses[role_id] = value

        return cleaned_data

    def save(self, created_by):
        """
        Вызывает фабрику и создаёт отчёт.
        """
        from reports.services.report_factory import ReportFactory

        factory = ReportFactory(
            resident=self.resident,
            created_by=created_by,
            date=self.date
        )

        return factory.create_or_update_report(
            data=self.cleaned_data,
            task_comments=self.task_comments,
            role_statuses=self.role_statuses
        )