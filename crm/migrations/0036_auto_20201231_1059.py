# Generated by Django 3.1.4 on 2020-12-31 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0035_auto_20201231_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='strike',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
    ]