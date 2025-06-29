from .character_trait_factory import CharacterTraitFactory


class CharacterTraitDefectFactory(CharacterTraitFactory):
    def get_verbose_name(self):
        return "Дефекты характера"

    def get_slug(self):
        return "charactertrait_defect"

    def get_trait_type(self):
        return "defect"
