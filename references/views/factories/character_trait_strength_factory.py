from .character_trait_factory import CharacterTraitFactory


class CharacterTraitStrengthFactory(CharacterTraitFactory):
    def get_verbose_name(self):
        return "Достоинства характера"

    def get_slug(self):
        return "charactertrait_strength"

    def get_trait_type(self):
        return "strength"