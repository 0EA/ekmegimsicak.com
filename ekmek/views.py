from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import EkmekForm, Vaziyet
from django.contrib import messages
from .models import Ekmek
import ekmek
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from . import tasks
from pusher_push_notifications import PushNotifications
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAA4Mbmo0I:APA91bGKs-uJQhBI9mig3XJnpuLUnQL8yoyZij9WGpR3ACtI7uHrH8RQCYVrk4DvYDLPoDE3CGrA0F8MwMI-5egC4SiTxbj2S67DzSxVagAq0JUBRjWZg-HSqRUH-8Yws34hLOQcsM3W")


# Create your views here.
@login_required(login_url=('user:login'))
def ekmekKontrol(request):
    ekmekler = Ekmek.objects.filter(uretici = request.user)
    context = {
        'ekmekler':ekmekler
    }
    return render(request, "ekmekKontrol.html", context=context)

@login_required(login_url=('user:login'))
def dashboard(request):
    ekmekler = Ekmek.objects.filter(uretici = request.user)
    context = {
        'ekmekler':ekmekler
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url=('user:login'))
def ekmekEkle(request):
    form = EkmekForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        ekmek = form.save(commit=False)
        ekmek.uretici = request.user
        ekmek.save()
        messages.success(request, 'Ekmek Turu Basariyla Eklendi.')
        ekmekler = Ekmek.objects.filter(uretici = request.user)
        context = {
        'ekmekler':ekmekler
        }
        return redirect('/ekmek/dashboard')
    
    return render(request, 'ekmekEkle.html', {'form':form})

@login_required(login_url=('user:login'))
def detay(request, id):
    #ekmek = Ekmek.objects.filter(id = id).first()
    ekmek = get_object_or_404(Ekmek, id=id)
    return render(request, 'detay.html', {'ekmek':ekmek})


@login_required(login_url=('user:login'))
def update(request, id):
    ekmek = get_object_or_404(Ekmek, id=id)
    form = EkmekForm(request.POST or None, request.FILES or None, instance=ekmek)

    if form.is_valid():
        ekmek = form.save(commit=False)
        ekmek.uretici = request.user
        ekmek.save()
        messages.success(request, 'Ekmek Turu Basariyla Guncellendi.')
        ekmekler = Ekmek.objects.filter(uretici = request.user)
        context = {
        'ekmekler':ekmekler
        }
        return redirect('/ekmek/dashboard')


    return render(request, 'update.html', {'form':form})

@login_required(login_url=('user:login'))
def delete(request, id):
    ekmek = get_object_or_404(Ekmek, id = id)
    ekmek.delete()

    messages.success(request, 'Ekmek Turu Basariyla Silindi')

    return redirect('/ekmek/dashboard')

def push_notify(uretici, ekmekAdi):

    beams_client = PushNotifications(
        instance_id='f2fa28f2-495b-4256-b8ef-c41fc34e9627',
        secret_key='4A5DE646C46789472704A8B1D5581BCA104329BB0A438DBD67132305BF656B5F',
    )
    response = beams_client.publish_to_interests(
    interests=['hello'],
    publish_body={
        'apns': {
            'aps': {
                'alert': 'Ekmek Çıkıyor!'
            }
        },
        'fcm': {
            'notification': {
                'title': str(uretici),
                'body': str('Sıcak ' + ekmekAdi + ' çıkıyor!')
                        }
                    }
                }
    )

    print(response['publishId'])
@login_required
def sicak(request, id):

    ekmek = get_object_or_404(Ekmek, id = id)

    #bildirimde kullanilacak
    now = datetime.now()
    ekmekTuru = ekmek.ekmekAdi
    uretici = ekmek.uretici
    ekmekID = ekmek.id
    ekmekAdi = ekmek.ekmekAdi
    ekmek.sonSicak = now.strftime("%d/%m/%Y %H:%M:%S")
    ekmek.save()
    tasks.setEkmekSoguk(id)
    messages.success(request, 'Ekmek Sicak Yayinlandi')
    message_title = str(uretici)
    message_body = "Sicak " + ekmekAdi + " cikiyor!"
    result = push_service.notify_topic_subscribers(topic_name=str(ekmekID), message_title=message_title, message_body=message_body)
    result2 = push_service.notify_topic_subscribers(topic_name= str(uretici.id) + '-' + str(ekmekID), message_title=message_title, message_body=message_body)
    

    return redirect('/ekmekKontrol')


@login_required
def vaziyet(request, id):
    ekmek = get_object_or_404(Ekmek, id=id)
    form = Vaziyet(request.POST or None, instance=ekmek)

    if form.is_valid():
        ekmek = form.save(commit=False)
        ekmek.uretici = request.user
        ekmek.save()
        messages.success(request, 'Ekmek Durumu Basariyla Guncellendi.')
        return redirect('/ekmekKontrol')

    return render(request, 'update.html', {'form':form})







    