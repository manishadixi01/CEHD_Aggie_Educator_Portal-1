# Generated by Django 4.0.3 on 2022-04-04 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('epp_student', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPlacements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_email', models.EmailField(default='', max_length=254)),
                ('university_supervisor_email', models.EmailField(max_length=254)),
                ('university_supervisor', models.CharField(max_length=100)),
                ('cooperating_teacher_email', models.EmailField(max_length=254)),
                ('cooperating_teacher', models.CharField(max_length=100)),
                ('principal', models.CharField(max_length=100)),
                ('site', models.CharField(max_length=50)),
                ('classroom_type', models.CharField(max_length=50)),
                ('semester', models.CharField(max_length=20)),
                ('field_experience_program', models.CharField(max_length=50)),
                ('placement', models.CharField(max_length=50)),
                ('beginning_date_experience', models.DateField()),
                ('ending_date_experience', models.DateField()),
                ('instructor', models.CharField(max_length=50)),
                ('eppstudent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='epp_student.eppstudent')),
                ('uin', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='sp_person', to='core.person', to_field='uin')),
            ],
            options={
                'db_table': 'student_placements',
                'unique_together': {('uin', 'semester')},
            },
        ),
    ]
