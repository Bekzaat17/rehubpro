# Generated by Django 5.2.3 on 2025-06-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0006_charactertrait_created_at_charactertrait_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailydynamics',
            name='score',
            field=models.IntegerField(default=0, verbose_name='Оценка'),
        ),
    ]
