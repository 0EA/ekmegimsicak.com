from django.db import models
from ckeditor.fields import RichTextField
from unixtimestampfield.fields import UnixTimeStampField

# Create your models here.

class Ekmek(models.Model):
    stokChoices = [
        ('Var', 'Var'),
        ('Yok', 'Yok'),
    ]

    durumChoices = [
        ('Sicak', 'Sicak'),
        ('Soguk', 'Soguk'),
        ('-', '-'),
    ]

    uretici = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = "Üretici")
    ekmekAdi = models.CharField(max_length=50, verbose_name="Ekmek Cinsi")
    ekmekDetayi = RichTextField(default='')
    sonSicak = models.CharField(max_length=40,blank=True, null=True, verbose_name='Sicak Cikis Tarihi', default='11/09/2020 14:24:36')

    

    def __str__(self):
        return self.ekmekAdi

