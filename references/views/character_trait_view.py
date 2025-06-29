from django.http import JsonResponse

from .base_reference_view import BaseReferenceView
from ..models.character_trait import CharacterTrait
from ..forms.character_trait_form import CharacterTraitForm

class CharacterTraitView(BaseReferenceView):
    """
    API-вьюха для справочника 'Чертa характера'.
    Обрабатывает GET, POST, DELETE.
    """
    model = CharacterTrait
    form_class = CharacterTraitForm

    def get(self, request):
        trait_type = request.GET.get("type")

        # Автоматически определяем тип, если не передали
        if not trait_type:
            if "strength" in request.path:
                trait_type = "strength"
            elif "defect" in request.path:
                trait_type = "defect"

        queryset = self.model.objects.filter(is_active=True)
        if trait_type in ["strength", "defect"]:
            queryset = queryset.filter(type=trait_type)

        data = list(queryset.values())
        return JsonResponse({'data': data})