# Generated by Django 5.0.9 on 2024-12-11 06:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('seaice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicGradTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'),
                             ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grad_month', models.IntegerField()),
                ('grad_type',
                 models.CharField(choices=[('sum', '海冰面积'), ('sqrt', '海冰变化')], default='sum', max_length=20)),
                ('result_urls', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '动力学分析任务',
                'verbose_name_plural': '动力学分析任务',
            },
        ),
        migrations.AlterModelOptions(
            name='downloadpredicttask',
            options={'verbose_name': '下载预测任务', 'verbose_name_plural': '下载预测任务'},
        ),
    ]
