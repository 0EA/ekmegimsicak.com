# Generated by Django 3.1 on 2020-08-15 22:24

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='primeColor',
            field=colorfield.fields.ColorField(default='#ffffff', max_length=18),
        ),
        migrations.AddField(
            model_name='profile',
            name='secColor',
            field=colorfield.fields.ColorField(default='#000000', max_length=18),
        ),
    ]
