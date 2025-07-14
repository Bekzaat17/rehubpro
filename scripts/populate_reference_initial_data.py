import os
from django.conf import settings
from slugify import slugify

from references.models import (
    EmotionalState, PhysicalState, FamilyActivity,
    MrpActivity, Motivation, DailyDynamics,
    CharacterTrait, ResidentRole
)


def safe_slugify(name):
    slug = slugify(name)
    return slug if slug else f"slug-{abs(hash(name))}"


def fill_if_missing(model, values):
    for name in values:
        slug = safe_slugify(name)
        model.objects.update_or_create(
            slug=slug,
            defaults={"name": name}
        )


def create_emotional_data():
    fill_if_missing(EmotionalState, [
        'Ровное', 'Тревожное', 'Раздражительное', 'Подавленное'
    ])
    fill_if_missing(PhysicalState, [
        'Хорошее', 'Удовлетворительное', 'Плохое'
    ])
    fill_if_missing(FamilyActivity, [
        'Высокая активность', 'Средняя активность', 'Пассивность', 'Отстранённость'
    ])
    fill_if_missing(MrpActivity, [
        'Активен', 'Умерен', 'Пассивен'
    ])
    fill_if_missing(Motivation, [
        'Положительная', 'Нейтральная', 'Отрицательная', 'Вынужденная'
    ])
    fill_if_missing(DailyDynamics, [
        'Положительная', 'Стабильная', 'Негативная'
    ])


def create_character_traits():
    traits = [
        ("безответственность", "defect"),
        ("безумие", "defect"),
        ("брезгливость", "defect"),
        ("воровство", "defect"),
        ("вспыльчивость", "defect"),
        ("высокомерие", "defect"),
        ("гордыня", "defect"),
        ("жалость к себе", "defect"),
        ("зависимость", "defect"),
        ("закрытость", "defect"),
        ("гиперконтроль", "defect"),
        ("интеллектуализация", "defect"),
        ("инфантильность", "defect"),
        ("изменчивость", "defect"),
        ("лень", "defect"),
        ("лицемерие", "defect"),
        ("ложь", "defect"),
        ("нечестность", "defect"),
        ("манипулятивность", "defect"),
        ("мнительность", "defect"),
        ("мстительность", "defect"),
        ("наглость", "defect"),
        ("негативное мышление", "defect"),
        ("неприспособленность", "defect"),
        ("несамодостаточность", "defect"),
        ("нетерпимость", "defect"),
        ("неуважение", "defect"),
        ("низкая самооценка", "defect"),
        ("одержимость", "defect"),
        ("отрицание", "defect"),
        ("предубеждённость", "defect"),
        ("пренебрежительность", "defect"),
        ("притворство", "defect"),
        ("подавление чувств", "defect"),
        ("раздражительность", "defect"),
        ("обида", "defect"),
        ("распущенность", "defect"),
        ("ревность", "defect"),
        ("самооправдание", "defect"),
        ("саморазрушение", "defect"),
        ("самоуверенность", "defect"),
        ("сарказм", "defect"),
        ("скрытность", "defect"),
        ("стереотипность", "defect"),
        ("собственничество", "defect"),
        ("самообман", "defect"),
        ("самодовольство", "defect"),
        ("хитрость", "defect"),
        ("занудство", "defect"),
        ("иллюзорность", "defect"),
        ("эгоцентризм", "defect"),
        ("эгоизм", "defect"),
        ("хамство", "defect"),
        ("гиперответственность", "defect"),
        ("зависть", "defect"),
        ("благодарность", "strength"),
        ("благоразумие", "strength"),
        ("вежливость", "strength"),
        ("вера", "strength"),
        ("верность", "strength"),
        ("весёлость", "strength"),
        ("взаимопомощь", "strength"),
        ("внимательность", "strength"),
        ("выносливость", "strength"),
        ("взаимопонимание", "strength"),
        ("гибкость", "strength"),
        ("готовность", "strength"),
        ("духовность", "strength"),
        ("жизнерадостность", "strength"),
        ("дисциплинированность", "strength"),
        ("доброжелательность", "strength"),
        ("забота", "strength"),
        ("искренность", "strength"),
        ("исполнительность", "strength"),
        ("коммуникабельность", "strength"),
        ("конструктивность", "strength"),
        ("кропотливость", "strength"),
        ("любовь", "strength"),
        ("мужественность", "strength"),
        ("мудрость", "strength"),
        ("мужество", "strength"),
        ("непредвзятость", "strength"),
        ("осторожность", "strength"),
        ("ответственность", "strength"),
        ("открытость", "strength"),
        ("позитивное мышление", "strength"),
        ("пунктуальность", "strength"),
        ("ритмичность", "strength"),
        ("смелость", "strength"),
        ("смирение", "strength"),
        ("собранность", "strength"),
        ("спокойствие", "strength"),
        ("талант", "strength"),
        ("терпимость", "strength"),
        ("трудолюбие", "strength"),
        ("уважительность", "strength"),
        ("ум", "strength"),
        ("щедрость", "strength"),
        ("целеустремлённость", "strength"),
        ("уравновешенность", "strength"),
    ]

    for name, type_ in traits:
        slug = safe_slugify(f"{type_}-{name}")
        CharacterTrait.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name,
                "type": type_,
            }
        )


def create_resident_roles():
    roles = [
        ("Президент", "president"),
        ("НСО", "nso"),
        ("ШК", "shk"),
        ("ХД", "hd"),
        ("Визор", "vizor"),
        ("Учетовед", "uchetoved"),
        ("Айболит", "aibolit"),
        ("Чайханщик", "chaikhanshchik"),
        ("Огородник", "ogorodnik"),
        ("ШРР", "shrr"),
        ("Фотокор", "fotokor"),
        ("БПК", "bpk"),
        ("Физорг", "fizorg"),
        ("Дискомен", "diskomen"),
        ("Библиотекарь", "bibliotekar"),
        ("Массовик Затейник", "massovik-zateynik"),
        ("Организаторы", "organizatory"),
        ("ХР.ВР.", "hr-vr"),
        ("Цветовод", "tsvetovod"),
        ("Животновод", "zhivotnovod"),
    ]
    for name, slug in roles:
        ResidentRole.objects.update_or_create(
            slug=slug,
            defaults={"name": name}
        )


def run():
    print("🔄 Populating initial reference data (safe)...")
    create_emotional_data()
    create_character_traits()
    create_resident_roles()
    print("✅ Initial reference data population complete.")


if __name__ == '__main__':
    run()