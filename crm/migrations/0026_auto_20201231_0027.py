# Generated by Django 3.1.4 on 2020-12-31 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0025_auto_20201231_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='checked',
            field=models.IntegerField(default=0),
        ),
    ]
