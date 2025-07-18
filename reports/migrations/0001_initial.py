# Generated by Django 5.2.3 on 2025-06-14 12:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('references', '0002_dailydynamics_emotionalstate_familyactivity_and_more'),
        ('residents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResidentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.localdate)),
                ('comment', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resident_reports_created', to=settings.AUTH_USER_MODEL)),
                ('daily_dynamics', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.dailydynamics')),
                ('emotional_state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.emotionalstate')),
                ('family_activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.familyactivity')),
                ('motivation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.motivation')),
                ('mrp_activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.mrpactivity')),
                ('negative_traits', models.ManyToManyField(blank=True, help_text='Отмеченные дефекты характера', related_name='negative_reports', to='references.charactertrait')),
                ('physical_state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='references.physicalstate')),
                ('positive_traits', models.ManyToManyField(blank=True, help_text='Отмеченные достоинства характера', related_name='positive_reports', to='references.charactertrait')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_reports', to='residents.resident')),
            ],
            options={
                'verbose_name': 'Ежедневный отчет',
                'verbose_name_plural': 'Ежедневные отчеты',
                'ordering': ['-date'],
                'unique_together': {('resident', 'date')},
            },
        ),
    ]
