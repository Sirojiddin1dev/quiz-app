# Generated by Django 4.2.9 on 2024-01-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customusers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='test_access',
            field=models.BooleanField(default=False),
        ),
    ]
