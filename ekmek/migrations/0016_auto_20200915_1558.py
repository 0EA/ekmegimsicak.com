# Generated by Django 3.1 on 2020-09-15 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekmek', '0015_auto_20200913_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ekmek',
            name='sonSicak',
            field=models.CharField(blank=True, default='11/09/2020 14:24:36', max_length=40, null=True, verbose_name='Sicak Cikis Tarihi'),
        ),
    ]
