# Generated by Django 3.1.4 on 2020-12-31 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20201228_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='habit',
            field=models.CharField(max_length=200, null=True),
        ),
    ]