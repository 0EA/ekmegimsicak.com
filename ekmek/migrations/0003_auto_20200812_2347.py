# Generated by Django 3.1 on 2020-08-12 20:47

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekmek', '0002_auto_20200812_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='ekmek',
            name='ekmekResmi',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Ekmek Resmi Ekle'),
        ),
        migrations.AlterField(
            model_name='ekmek',
            name='ekmekDetayi',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]
