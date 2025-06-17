
# reports/forms/resident_report_form.py
from django import forms
from django.db import models # For Q objects
from references.models.character_trait import TraitType

from references.repositories import (
    EmotionalStateRepository, PhysicalStateRepository, MotivationRepository,
    DailyDynamicsRepository, MrpActivityRepository, FamilyActivityRepository,
    CharacterTraitRepository
)
# Import the aliased versions for ResidentRole from references.models
# from references.repositories import ReferenceResidentRoleRepository # Not used directly in this form yet

# We will also need repositories for tasks and roles for _init_dynamic_fields in the future.
# For now, those parts of _init_dynamic_fields remain unchanged.

class ResidentReportForm(forms.Form):
    emotional_state = forms.ModelChoiceField(queryset=None, label="Эмоциональное состояние")
    physical_state = forms.ModelChoiceField(queryset=None, label="Физическое состояние")
    motivation = forms.ModelChoiceField(queryset=None, label="Мотивация")
    daily_dynamics = forms.ModelChoiceField(queryset=None, label="Динамика")

    positive_traits = forms.ModelMultipleChoiceField(
        queryset=None, required=False, widget=forms.CheckboxSelectMultiple, label="Достоинства"
    )
    negative_traits = forms.ModelMultipleChoiceField(
        queryset=None, required=False, widget=forms.CheckboxSelectMultiple, label="Дефекты"
    )

    mrp_activity = forms.ModelChoiceField(queryset=None, required=False, label="Участие в МРП")
    family_activity = forms.ModelChoiceField(queryset=None, required=False, label="Семейное взаимодействие")

    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        required=False, label="Общий комментарий"
    )

    def __init__(self, *args,
                 # Repositories for reference models
                 emotional_state_repo: EmotionalStateRepository,
                 physical_state_repo: PhysicalStateRepository,
                 motivation_repo: MotivationRepository,
                 daily_dynamics_repo: DailyDynamicsRepository,
                 character_trait_repo: CharacterTraitRepository,
                 mrp_activity_repo: MrpActivityRepository,
                 family_activity_repo: FamilyActivityRepository,
                 # resident and date are passed from the view/service
                 resident=None, date=None,
                 # TODO: Add other needed repos for tasks, roles once they are created
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.resident = resident
        self.date = date

        # Store repos for reference models
        self.emotional_state_repo = emotional_state_repo
        self.physical_state_repo = physical_state_repo
        self.motivation_repo = motivation_repo
        self.daily_dynamics_repo = daily_dynamics_repo
        self.character_trait_repo = character_trait_repo
        self.mrp_activity_repo = mrp_activity_repo
        self.family_activity_repo = family_activity_repo

        # Populate querysets using repositories
        if self.emotional_state_repo:
            self.fields["emotional_state"].queryset = self.emotional_state_repo.list_all()
        if self.physical_state_repo:
            self.fields["physical_state"].queryset = self.physical_state_repo.list_all()
        if self.motivation_repo:
            self.fields["motivation"].queryset = self.motivation_repo.list_all()
        if self.daily_dynamics_repo:
            self.fields["daily_dynamics"].queryset = self.daily_dynamics_repo.list_all()
        if self.mrp_activity_repo:
            self.fields["mrp_activity"].queryset = self.mrp_activity_repo.list_all()
        if self.family_activity_repo:
            self.fields["family_activity"].queryset = self.family_activity_repo.list_all()

        if self.character_trait_repo:
            self.fields["positive_traits"].queryset = self.character_trait_repo.list_by_type(TraitType.STRENGTH)
            self.fields["negative_traits"].queryset = self.character_trait_repo.list_by_type(TraitType.DEFECT)

        self.task_comments = {}
        self.role_statuses = {}
        # _init_dynamic_fields still uses direct ORM calls for tasks and roles.
        # This will be addressed when we refactor those apps.
        self._init_dynamic_fields()

        self.fields["usts_info_shared"] = forms.ChoiceField(
            label="Информацию подает УСТС:",
            choices=[("true", "Ровно"), ("false", "Не ровно")],
            widget=forms.RadioSelect, required=False
        )
        self.fields["usts_format_followed"] = forms.ChoiceField(
            label="Имеет формат УСТС:",
            choices=[("true", "Имеет"), ("false", "Не имеет")],
            widget=forms.RadioSelect, required=False
        )
        self.fields["usts_comment"] = forms.CharField(
            label="Комментарий по УТС", required=False,
            widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
        )

    def _init_dynamic_fields(self):
        # This part still uses direct ORM calls.
        # It will be refactored when 'tasks' and 'roles' apps are processed.
        from tasks.models.assigned_task import AssignedTask
        from roles.models.resident_role_assignment import ResidentRoleAssignment

        active_tasks = AssignedTask.objects.filter(
            resident=self.resident,
            status__in=["writing", "submitting"]
        )
        for task in active_tasks:
            field_name = f"task_comment_{task.id}"
            self.fields[field_name] = forms.CharField(
                label=f"Комментарий к задаче: {task.task.title}",
                required=False,
                widget=forms.Textarea(attrs={"rows": 2, "class": "form-control"})
            )

        active_roles = ResidentRoleAssignment.objects.filter(
            resident=self.resident,
            assigned_at__lte=self.date
        ).filter(
            models.Q(unassigned_at__isnull=True) | models.Q(unassigned_at__gte=self.date)
        ).distinct()

        for role_assignment in active_roles:
            field_name = f"role_status_{role_assignment.id}"
            self.fields[field_name] = forms.ChoiceField(
                label=f"Роль: {role_assignment.role.name}",
                choices=[
                    ("responsible", "Ответственный"),
                    ("irresponsible", "Безответственный")
                ],
                widget=forms.RadioSelect
            )

    def clean(self):
        cleaned_data = super().clean()
        for field in ["usts_info_shared", "usts_format_followed"]:
            value = cleaned_data.get(field)
            if value == "true": cleaned_data[field] = True
            elif value == "false": cleaned_data[field] = False
            else: cleaned_data[field] = None

        self.task_comments = {}
        for name, value in self.cleaned_data.items():
            if name.startswith("task_comment_") and value:
                stripped_value = value.strip()
                if stripped_value:
                    task_id = int(name.split("_")[-1])
                    self.task_comments[task_id] = stripped_value

        self.role_statuses = {}
        for name, value in self.cleaned_data.items():
            if name.startswith("role_status_") and value:
                role_id = name.split("_")[-1]
                self.role_statuses[role_id] = value
        return cleaned_data

    def save(self, created_by):
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
