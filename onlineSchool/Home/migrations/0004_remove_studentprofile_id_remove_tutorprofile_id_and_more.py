# Generated by Django 5.0.1 on 2025-06-09 12:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_user_is_admin_user_is_student_user_is_tutor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tutorprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
