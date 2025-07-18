from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import os

from references.models import (
    EmotionalState, PhysicalState, FamilyActivity,
    MrpActivity, Motivation, DailyDynamics,
    CharacterTrait, ResidentRole
)

from slugify import slugify


class Command(BaseCommand):
    help = "Populate initial reference and system data"

    def safe_slugify(self, name):
        slug = slugify(name)
        return slug if slug else f"slug-{abs(hash(name))}"

    def fill_if_missing_with_score(self, model, values_with_scores):
        for name, score in values_with_scores:
            slug = self.safe_slugify(name)
            model.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "score": score}
            )

    def create_emotional_data(self):
        self.fill_if_missing_with_score(EmotionalState, [
            ('Ровное', 80),
            ('Тревожное', 40),
            ('Раздражительное', 30),
            ('Подавленное', 20)
        ])
        self.fill_if_missing_with_score(PhysicalState, [
            ('Хорошее', 90),
            ('Удовлетворительное', 60),
            ('Плохое', 30)
        ])
        self.fill_if_missing_with_score(FamilyActivity, [
            ('Высокая активность', 90),
            ('Средняя активность', 60),
            ('Пассивность', 30),
            ('Отстранённость', 10)
        ])
        self.fill_if_missing_with_score(MrpActivity, [
            ('Активен', 90),
            ('Умерен', 60),
            ('Пассивен', 30)
        ])
        self.fill_if_missing_with_score(Motivation, [
            ('Положительная', 90),
            ('Нейтральная', 50),
            ('Отрицательная', 20),
            ('Вынужденная', 10)
        ])
        self.fill_if_missing_with_score(DailyDynamics, [
            ('Положительная', 90),
            ('Стабильная', 60),
            ('Негативная', 30)
        ])

    def create_character_traits(self):
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
            slug = self.safe_slugify(f"{type_}-{name}")
            CharacterTrait.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "type": type_}
            )

    def create_resident_roles(self):
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

    def create_superuser_if_missing(self):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write("⚙️ Создание суперпользователя...")

            username = os.getenv("SUPERUSER_USERNAME", "admin")
            email = os.getenv("SUPERUSER_EMAIL", "admin@example.com")
            password = os.getenv("SUPERUSER_PASSWORD", "admin")

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Суперпользователь {username} создан."))
        else:
            self.stdout.write("✅ Суперпользователь уже существует — пропускаем.")

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Populating initial reference data...")

        self.create_emotional_data()
        self.create_character_traits()
        self.create_resident_roles()
        self.create_superuser_if_missing()

        self.stdout.write(self.style.SUCCESS("✅ All reference data loaded successfully."))