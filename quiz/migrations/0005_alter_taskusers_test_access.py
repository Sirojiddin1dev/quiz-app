# Generated by Django 4.2.9 on 2024-01-21 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_taskusers_test_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskusers',
            name='test_access',
            field=models.BooleanField(default=False),
        ),
    ]
