from django import forms
from .models import Ekmek

class EkmekForm(forms.ModelForm):
    class Meta:
        model = Ekmek
        fields = ['ekmekAdi', 'ekmekDetayi', 'ekmekResmi', 'stok', 'durum', 'sonSicak',]


class Vaziyet(forms.ModelForm):
    class Meta:
        model = Ekmek
        fields = ['stok', 'durum', 'sonSicak',]
