from django.db import models
from ckeditor.fields import RichTextField

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
    stok = models.CharField(max_length=3,choices=stokChoices, default='Yok')
    durum = models.CharField(max_length=5, choices=durumChoices, default='Soguk')
    ekmekResmi = models.ImageField(blank=True, null=True, verbose_name='Ekmek Resmi Ekle', upload_to='ekmek/')
    sonSicak = models.CharField(max_length=40,blank=True, null=True, verbose_name='Son Sicak Cikis Tarihi')

    

    def __str__(self):
        return self.ekmekAdi

