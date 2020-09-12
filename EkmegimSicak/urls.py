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
from ekmek import views as ekmekViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('user/', include('user.urls')),
    path('ekmek/', include('ekmek.urls')),
    path('ekmekKontrol/', ekmekViews.ekmekKontrol, name="ekmekKontrol"),
    path('info/', views.info, name='info'),
    path('filtreJson/', views.filtreJson, name = 'filtreJson'),
    path('firmalarJson/', views.firmalarJson, name='firmalarJson'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
