from django.contrib import admin
from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('profil/<int:id>', views.profil, name='profil'),
    path('profilEdit/<int:id>', views.profilEdit, name='profilEdit'),
]