# Generated by Django 4.2.9 on 2024-02-10 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customusers', '0006_alter_customuser_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 10, 14, 35, 39, 343308, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]