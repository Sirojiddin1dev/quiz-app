# Generated by Django 4.2.9 on 2024-05-29 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_task_options_task_global_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['category']},
        ),
        migrations.RemoveField(
            model_name='task',
            name='global_order',
        ),
        migrations.RemoveField(
            model_name='task',
            name='order',
        ),
    ]
