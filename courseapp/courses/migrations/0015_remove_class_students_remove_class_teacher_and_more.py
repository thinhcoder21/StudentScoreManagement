# Generated by Django 4.2.6 on 2024-02-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_teacher_student_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='students',
        ),
        migrations.RemoveField(
            model_name='class',
            name='teacher',
        ),
        migrations.AddField(
            model_name='class',
            name='account',
            field=models.ManyToManyField(blank=True, related_name='classes_enrolled', to='courses.account'),
        ),
    ]
