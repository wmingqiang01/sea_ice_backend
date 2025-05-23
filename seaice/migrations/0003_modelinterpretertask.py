# Generated by Django 5.0.8 on 2025-03-22 05:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('seaice', '0002_dynamicgradtask_alter_downloadpredicttask_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelInterpreterTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'),
                             ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grad_day', models.IntegerField()),
                ('grad_type',
                 models.CharField(choices=[('sum', '海冰面积'), ('l2', 'L2范数')], default='sum', max_length=20)),
                ('result_urls', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '模型可解释性任务',
                'verbose_name_plural': '模型可解释性任务',
            },
        ),
    ]
