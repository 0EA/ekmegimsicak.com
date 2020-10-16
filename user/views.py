from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.html import strip_tags
from .models import Profile
import json
import time
import datetime
from datetime import datetime, timedelta
import pyrebase
from operator import itemgetter
from pusher_push_notifications import PushNotifications
from pyfcm import FCMNotification

config = {
  "apiKey": "AIzaSyC8sQuCoPr854RbIJlpFFrrIHUrlQecTtE",
  "authDomain": "ekmegimsicak.firebaseapp.com",
  "databaseURL": "https://ekmegimsicak.firebaseio.com/",
  "storageBucket": "ekmegimsicak.appspot.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
push_service = FCMNotification(api_key="AAAA4Mbmo0I:APA91bGKs-uJQhBI9mig3XJnpuLUnQL8yoyZij9WGpR3ACtI7uHrH8RQCYVrk4DvYDLPoDE3CGrA0F8MwMI-5egC4SiTxbj2S67DzSxVagAq0JUBRjWZg-HSqRUH-8Yws34hLOQcsM3W")



def isLogged():
    current_user = auth.current_user
    if current_user != None:
        return True
    else:
        return False
def girisGerekli(func):
    def inner(request):
        if isLogged():
            return func(request)
        else:
            messages.info(request, 'Lütfen önce giriş yapın.')
            return redirect('user:login')
    return inner




def loginUser(request):
    if isLogged():
        return redirect('ekmekKontrol')
    form = LoginForm(request.POST or None)
    context = {
        'form':form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = username + '@ekmegimsicak.com'
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return redirect('ekmekKontrol')
        except:
            messages.info(request, 'Kullanici adi veya sifre hatali, lutfen tekrar deneyin.')
            return render(request, 'login.html', context)     
    return render(request,'login.html',context)

@girisGerekli
def logoutUser(request):
    auth.current_user = None
    messages.success(request, "Başarıyla çıkış yaptınız")
    return redirect('user:login')



def sicakDurum(firinSonSicak):
    dakika = firinSonSicak[1]
    dakika = abs(dakika)
    degisken = 'dakika'
    if len(str(dakika)) >= 3:
        dakika = dakika//60
        degisken = 'saat'
    if firinSonSicak[1] > 0:
        firinSonSicak.append("#BA0036")
        return (str(abs(dakika)) + ' ' + degisken + ' sonra ' + firinSonSicak[0] + ' çıkıyor.')
    elif firinSonSicak[1] > -10:
        firinSonSicak.append("#BA0036")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + firinSonSicak[0] + ' çıktı.')
    elif firinSonSicak[1] > -45:
        firinSonSicak.append("#ff5803")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + firinSonSicak[0] + ' çıktı.')
    else:
        firinSonSicak.append("#2861ac")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + firinSonSicak[0] + ' çıktı.')
def firinlar(request):
    keyword = request.GET.get("keyword")
    db = firebase.database()
    result = db.child("profiles").get().val()
    result = dict(result)
    timestamp = time.time()
    for firinAdi,firin in result.items():
        firin['firinSonSicak'][1] = int((firin['firinSonSicak'][1] - timestamp) // 60)
        firin['firinSonSicak'][1] = sicakDurum(firin['firinSonSicak'])
    
    if keyword:
        for firinAdi, i in result.items():
            firinIsim = str(i['name']).lower()
            if str(keyword).lower() in firinIsim:
                
                context={
                    'firinlar':{firinAdi:i}.items()
                }
                return render(request, "firinlar.html", context=context)
            else:
                context={
                'firinlar':result.items(),
                }
                messages.info(request, "Maalesef aradığınız isme sahip fırın şu anda bulunmuyor :(")
                return render(request, "firinlar.html", context=context)
    context={
        'firinlar':result.items(),
    }
    return render(request, 'firinlar.html', context=context)



def saat_renk(sonSicakObjesi):
    dakika = sonSicakObjesi[0]
    dakika = abs(dakika)
    degisken = 'dakika'
    if len(str(dakika)) >= 3:
        dakika = dakika//60
        degisken = 'saat'
    if sonSicakObjesi[0] > 0:
        sonSicakObjesi[1] = ("#cc4a46")
        return (str(abs(dakika)) + ' ' + degisken + ' sonra ' + ' çıkıyor.')
    elif sonSicakObjesi[0] > -10:
        sonSicakObjesi[1] = ("#cc4a46")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + ' çıktı.')
    elif sonSicakObjesi[0] > -45:
        sonSicakObjesi[1] = ("#ff5803")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + ' çıktı.')
    else:
        sonSicakObjesi[1] = ("#4986D4")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + ' çıktı.')
def detay(request, name):
    db = firebase.database()
    firin = db.child("profiles").child(name).get().val()
    suan = time.time()
    firin['ekmekler'] = sorted(firin['ekmekler'].values(), key=itemgetter('sonSicak'), reverse=True)


    for ekmek in firin['ekmekler']:
        ekmek['sonSicak'] = [int((ekmek['sonSicak'] - suan) // 60), 'renk', ekmek['ekmekAdi']]
        ekmek['sonSicak'][0] = saat_renk(ekmek['sonSicak'])

    context = {
        'firin':firin
    }
    return render(request, 'detay.html', context=context)




def index(request):
    return render(request, "index-agency-musteri.html")

def info(request):
    return render(request, "index-agency-firin.html")






def newhandler404(request, exception):
    return render(request, '404.html', status=404)
def newhandler500(request):
    return render(request, '500.html', status=500)



def userInfo_username():
    user = auth.current_user
    email = user['email']
    username = email.split('@')[0]
    return username

@girisGerekli
def ekmekKontrol(request):
    user_username = userInfo_username()
    db = firebase.database()
    firin = db.child("profiles").child(user_username).get().val()
    suan = time.time()
    firin['ekmekler'] = sorted(firin['ekmekler'].values(), key=itemgetter('sonSicak'), reverse=True)


    for ekmek in firin['ekmekler']:
        ekmek['sonSicak'] = [int((ekmek['sonSicak'] - suan) // 60), 'renk', ekmek['ekmekAdi']]
        ekmek['sonSicak'][0] = saat_renk(ekmek['sonSicak'])
    context = {
        'firin':firin
    }
    return render(request, "ekmekKontrol.html", context=context)



def sicakCikar(request, firinAdi, ekmekId):
    if auth.current_user != None:
        if request.method == 'POST':
            dakika = request.POST.get('dakika')
            duration = request.POST.get('duration')
            bildirim = request.POST.get('bildirim', 'off')
            print(duration)

            if int(dakika) < 0:
                messages.info(request, 'Maalesef Bir Sikinti Olustu')
                return redirect('ekmekKontrol')

            now = datetime.now().timestamp()
            yeniTarih = int(now) + (int(dakika)*60)



            
            db = firebase.database()
            db.child("profiles").child(firinAdi).child("ekmekler").child(ekmekId).update({"sonSicak":yeniTarih})
            db.child("profiles").child(firinAdi).child("firinSonSicak").update({"1":yeniTarih})
            firinIsmi = db.child("profiles/" + firinAdi + "/ekmekler/" + str(ekmekId) + "/name").get().val()
            ekmekIsmi = db.child("profiles/" + firinAdi + "/ekmekler/" + str(ekmekId) + "/ekmekAdi").get().val()

            if int(duration) != 0:
                db.child("profiles").child(firinAdi).child("ekmekler").child(ekmekId).update({"duration":int(now)+int(duration)*60})

            message_title = str(firinIsmi)
            message_body = str(dakika) + " dakika sonra sıcak " + str(ekmekIsmi) + " çıkıyor!"
            if int(dakika) == 0:
                message_body = "Sıcak " + str(ekmekIsmi) + " çıkıyor!"
                dakika = 5 * 60

            data_message = {
            "sender": firinAdi,
            "ekmekId" : ekmekId,
            "timestamp" : yeniTarih,
            "title": message_title,
            "message": message_body
            }

            if bildirim == 'on':
                result = push_service.notify_topic_subscribers(topic_name= str(firinAdi) + '-' + str(ekmekId), data_message=data_message, content_available=True, time_to_live=int(dakika))
                messages.success(request, 'Bildirim Basari Ile Yayinlandi')
            else:
                messages.success(request, 'Ekmek Basari Ile Sicak Olarak Yayinlandi')
            return redirect('ekmekKontrol')


        else:
            db = firebase.database()
            user_username = userInfo_username()
            suan = time.time()
            ekmek = db.child("profiles").child(user_username).child("ekmekler").child(str(ekmekId)).get().val()
            ekmek = dict(ekmek)
            ekmek['sonSicak'] = [int((ekmek['sonSicak'] - suan) // 60), 'renk', ekmek['ekmekAdi']]
            ekmek['sonSicak'][0] = saat_renk(ekmek['sonSicak'])
            return render(request,'sicakCikar.html', context=ekmek)

    
    messages.success(request, "Lutfen Once Giris Yapiniz")
    return redirect('user:login')
    
    
           
    