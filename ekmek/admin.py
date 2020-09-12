from django.contrib import admin

from .models import Ekmek
# Register your models here.

@admin.register(Ekmek)
class EkmekAdmin(admin.ModelAdmin):

    list_display = ["ekmekAdi",]

    class Meta:
        model = Ekmek

