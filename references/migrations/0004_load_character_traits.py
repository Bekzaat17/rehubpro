from django.db import migrations
from slugify import slugify


def create_character_traits(apps, schema_editor):
    CharacterTrait = apps.get_model("references", "CharacterTrait")

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
        CharacterTrait.objects.create(
            name=name,
            type=type_,
            slug=slugify(f"{type_}-{name}")
        )


def delete_character_traits(apps, schema_editor):
    CharacterTrait = apps.get_model("references", "CharacterTrait")
    CharacterTrait.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("references", "0003_load_initial_data"),
    ]

    operations = [
        migrations.RunPython(create_character_traits, delete_character_traits),
    ]