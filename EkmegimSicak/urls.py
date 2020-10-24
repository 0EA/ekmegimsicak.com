"""EkmegimSicak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('info/', views.info, name='info'),
    path('user/', include('user.urls')),
    path('firinlar/', views.firinlar, name='firinlar'),
    path('detay/<str:name>', views.detay, name='detay'),
    path('ekmekKontrol/', views.ekmekKontrol, name="ekmekKontrol"),
    path('<str:firinAdi>/<str:ekmekId>/', views.sicakCikar, name="sicakCikar"),
]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
