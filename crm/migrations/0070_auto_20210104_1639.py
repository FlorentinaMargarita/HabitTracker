# Generated by Django 3.1.4 on 2021-01-05 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0069_auto_20210104_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='predefinedHabit',
        ),
        migrations.RemoveField(
            model_name='order',
            name='strikeList',
        ),
        migrations.DeleteModel(
            name='Count',
        ),
    ]