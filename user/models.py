from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilResmi = models.ImageField(blank=True, null=True, verbose_name='Profil Resmi Ekle', upload_to='profil/', default='/static/finalLogo.png')
    aciklama = RichTextField(default='')
    telefonNumarasi = models.IntegerField(null=True, blank=True)
    primeColor = ColorField(default='#ffffff')
    secColor = ColorField(default='#000000')
    adres = models.CharField(default='Kayitli Adres Bulunmuyor', max_length=150)
    long = models.DecimalField(max_digits=9, decimal_places=6, default=00)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=00)


