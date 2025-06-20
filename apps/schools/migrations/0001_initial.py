# Generated by Django 5.2.2 on 2025-06-13 17:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=1)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='schools.school')),
            ],
            options={
                'ordering': ['school', 'order'],
                'unique_together': {('school', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.unit')),
            ],
            options={
                'unique_together': {('student', 'module')},
            },
        ),
    ]
