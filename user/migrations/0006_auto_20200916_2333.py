# Generated by Django 3.1 on 2020-09-16 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200913_0022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='long',
            new_name='longitude',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='primeColor',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='secColor',
        ),
    ]
