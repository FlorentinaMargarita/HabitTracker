# Generated by Django 3.1.4 on 2020-12-31 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_auto_20201230_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='habit',
            field=models.CharField(choices=[('Call Mum', 'Call Mum'), ('Workout', 'Workout'), ('Buy Groceries', 'Buy Groceries'), ('Study Maths', 'Study Maths'), ('Meditate', 'Meditate')], max_length=200, null=True),
        ),
    ]
