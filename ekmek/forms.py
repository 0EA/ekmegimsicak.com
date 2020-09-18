from django import forms
from django.db import models
from ckeditor.fields import RichTextField
from unixtimestampfield.fields import UnixTimeStampField


class EkmekForm(forms.Form):
    ekmekAdi = models.CharField(max_length=50, verbose_name="Ekmek Cinsi")
    ekmekDetayi = RichTextField(default='')
    sonSicak = models.CharField(max_length=40,blank=True, null=True, verbose_name='Sicak Cikis Tarihi', default='11/09/2020 14:24:36')


class Vaziyet(forms.Form):
    sonSicak = models.CharField(max_length=40,blank=True, null=True, verbose_name='Sicak Cikis Tarihi', default='11/09/2020 14:24:36')
