# Generated by Django 3.1 on 2020-08-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekmek', '0004_auto_20200813_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='ekmek',
            name='sonSicak',
            field=models.DateField(blank=True, null=True),
        ),
    ]
