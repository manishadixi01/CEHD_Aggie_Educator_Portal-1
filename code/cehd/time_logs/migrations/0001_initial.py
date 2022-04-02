# Generated by Django 4.0.3 on 2022-03-31 06:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_placements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_date', models.DateField()),
                ('notes', models.TextField(default='')),
                ('hours_submitted', models.PositiveIntegerField(default=0)),
                ('hours_approved', models.BooleanField()),
                ('approval_due_date', models.DateField()),
                ('semester', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('date_submitted', models.DateField(default=datetime.date.today)),
                ('student_placements', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='placements', to='student_placements.studentplacements')),
                ('student_uin', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='student_uid', to='student_placements.studentplacements', to_field='uin')),
            ],
            options={
                'db_table': 'time_logs',
                'unique_together': {('student_uin', 'log_date')},
            },
        ),
    ]
