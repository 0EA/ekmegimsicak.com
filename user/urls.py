from django.contrib import admin
from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('yardim/<str:firinAdi>', views.yardim, name='yardim'),
    path('changeUserSettings/<str:firinAdi>', views.changeUserSettings, name='changeUserSettings'),
    path('changeProfile/<str:firinAdi>', views.changeProfile, name='changeProfile'),

]