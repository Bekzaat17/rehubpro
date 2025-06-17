# reports/factories/resident_report_form_factory.py

from reports.forms.resident_report_form import ResidentReportForm
from references.repositories import (
    DjangoEmotionalStateRepository,
    DjangoPhysicalStateRepository,
    DjangoMotivationRepository,
    DjangoDailyDynamicsRepository,
    DjangoCharacterTraitRepository,
    DjangoMrpActivityRepository,
    DjangoFamilyActivityRepository
)
# Import any other repositories that ResidentReportForm might need in the future
# (e.g., for tasks, roles)


class ResidentReportFormFactory:
    def __init__(self):
        # Instantiate repositories once if they are stateless
        # Or, if they need request-specific info (unlikely for these reference repos),
        # they could be instantiated per 'create' call or take 'request' in 'create'.
        # For now, assuming they are stateless.
        self.emotional_state_repo = DjangoEmotionalStateRepository()
        self.physical_state_repo = DjangoPhysicalStateRepository()
        self.motivation_repo = DjangoMotivationRepository()
        self.daily_dynamics_repo = DjangoDailyDynamicsRepository()
        self.character_trait_repo = DjangoCharacterTraitRepository()
        self.mrp_activity_repo = DjangoMrpActivityRepository()
        self.family_activity_repo = DjangoFamilyActivityRepository()
        # Initialize other repositories here if needed by the form

    def create(self, resident, date, request_data=None, initial_data=None):
        """
        Creates and returns an instance of ResidentReportForm,
        injecting all necessary repository dependencies.

        Args:
            resident: The resident object for the report.
            date: The date for the report.
            request_data: Optional dictionary-like data, typically request.POST for bound forms.
            initial_data: Optional dictionary for initial form values (for unbound forms).
        """
        form_kwargs = {
            'resident': resident,
            'date': date,
            'emotional_state_repo': self.emotional_state_repo,
            'physical_state_repo': self.physical_state_repo,
            'motivation_repo': self.motivation_repo,
            'daily_dynamics_repo': self.daily_dynamics_repo,
            'character_trait_repo': self.character_trait_repo,
            'mrp_activity_repo': self.mrp_activity_repo,
            'family_activity_repo': self.family_activity_repo,
            # Add other repositories here
        }

        if initial_data:
            form_kwargs['initial'] = initial_data

        if request_data:
            # For bound forms, pass request_data as the first argument
            return ResidentReportForm(request_data, **form_kwargs)
        else:
            # For unbound forms (e.g., for GET requests with initial data)
            return ResidentReportForm(**form_kwargs)
