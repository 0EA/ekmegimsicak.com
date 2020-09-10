from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilResmi = models.ImageField(blank=True, null=True, verbose_name='Profil Resmi Ekle', upload_to='profil/')
    aciklama = RichTextField(default='')
    telefonNumarasi = models.IntegerField(null=True,default=True)
    primeColor = ColorField(default='#ffffff')
    secColor = ColorField(default='#000000')

