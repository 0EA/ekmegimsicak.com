from django.contrib import admin
from django.urls import path

from . import views
from ekmek.views import ekmekKontrol

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path("ekmekEkle/", views.ekmekEkle, name="ekmekEkle"),
    path("detay/<int:id>", views.detay, name="detay"),
    path("update/<int:id>", views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    path('sicak/<int:id>', views.sicak, name='sicak'),
    path("vaziyet/<int:id>", views.vaziyet, name="vaziyet"),
    path("ekmekKontrol/", ekmekKontrol, name="ekmekKontrol")
    
]
