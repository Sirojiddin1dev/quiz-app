# Generated by Django 4.2.9 on 2024-02-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customusers', '0002_customuser_test_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='test_access',
            field=models.IntegerField(choices=[(0, 'no_access'), (1, 'first_second'), (2, 'trird'), (4, 'all')], default=0),
        ),
    ]