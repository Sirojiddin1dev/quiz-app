# Generated by Django 5.0 on 2023-12-23 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='timer',
            field=models.IntegerField(default=1),
        ),
    ]
