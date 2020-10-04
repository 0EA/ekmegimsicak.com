from django import forms
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Şifre", widget = forms.PasswordInput)