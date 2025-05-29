from django.db import migrations

def create_initial_resident_roles(apps, schema_editor):
    ResidentRole = apps.get_model("references", "ResidentRole")
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
        ResidentRole.objects.create(name=name, slug=slug)

def delete_initial_resident_roles(apps, schema_editor):
    ResidentRole = apps.get_model("references", "ResidentRole")
    slugs = [
        "president", "nso", "shk", "hd", "vizor", "uchetoved", "aibolit",
        "chaikhanshchik", "ogorodnik", "shrr", "fotokor", "bpk", "fizorg",
        "diskomen", "bibliotekar", "massovik-zateynik", "organizatory",
        "hr-vr", "tsvetovod", "zhivotnovod",
    ]
    ResidentRole.objects.filter(slug__in=slugs).delete()

class Migration(migrations.Migration):

    dependencies = [
        ("references", "0004_load_character_traits"),
    ]

    operations = [
        migrations.RunPython(create_initial_resident_roles, delete_initial_resident_roles),
    ]