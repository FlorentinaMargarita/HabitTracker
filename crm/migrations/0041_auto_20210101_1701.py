# Generated by Django 3.1.4 on 2021-01-02 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0040_auto_20210101_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='count',
            name='time_saved',
        ),
        migrations.AlterField(
            model_name='count',
            name='start_time',
            field=models.DateTimeField(auto_now=True, verbose_name='date published'),
        ),
    ]