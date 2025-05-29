from django.db import migrations
from slugify import slugify


def load_initial_reference_data(apps, schema_editor):
    def safe_slugify(name):
        slug = slugify(name)
        return slug if slug else f"slug-{abs(hash(name))}"

    def reset_and_fill(model_name, values):
        model = apps.get_model('references', model_name)
        model.objects.all().delete()
        model.objects.bulk_create([
            model(name=name, slug=safe_slugify(name)) for name in values
        ])

    reset_and_fill('EmotionalState', [
        'Ровное', 'Тревожное', 'Раздражительное', 'Подавленное'
    ])
    reset_and_fill('PhysicalState', [
        'Хорошее', 'Удовлетворительное', 'Плохое'
    ])
    reset_and_fill('FamilyActivity', [
        'Высокая активность', 'Средняя активность', 'Пассивность', 'Отстранённость'
    ])
    reset_and_fill('MrpActivity', [
        'Активен', 'Умерен', 'Пассивен'
    ])
    reset_and_fill('Motivation', [
        'Положительная', 'Нейтральная', 'Отрицательная', 'Вынужденная'
    ])
    reset_and_fill('DailyDynamics', [
        'Положительная', 'Стабильная', 'Негативная'
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0002_dailydynamics_emotionalstate_familyactivity_and_more'),
    ]

    operations = [
        migrations.RunPython(load_initial_reference_data),
    ]