# Generated by Django 5.0.9 on 2024-11-12 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seaice', '0002_downloadpredicttask_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadpredicttask',
            name='input_files',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
