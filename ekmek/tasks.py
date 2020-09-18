from background_task import background
from django.shortcuts import get_object_or_404


@background(schedule=60*15)
def setEkmekSoguk(id):
    #ekmek = get_object_or_404(Ekmek, id = id)
    #ekmek.durum = 'Soguk'
    #ekmek.save()
    pass