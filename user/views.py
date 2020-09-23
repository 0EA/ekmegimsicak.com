from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.html import strip_tags
from .models import Profile
import json
import time
import datetime
import pyrebase
from operator import itemgetter


config = {
  "apiKey": "AIzaSyC8sQuCoPr854RbIJlpFFrrIHUrlQecTtE",
  "authDomain": "ekmegimsicak.firebaseapp.com",
  "databaseURL": "https://ekmegimsicak.firebaseio.com/",
  "storageBucket": "ekmegimsicak.appspot.com"
}

firebase = pyrebase.initialize_app(config)

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('ekmekKontrol')
        #ekmekler = Ekmek.objects.filter(uretici = request.user)
        #context = {
        #'ekmekler':ekmekler
        #}
        #return render(request, "ekmekKontrol.html", context=context)
    form = LoginForm(request.POST or None)

    context = {
        'form':form
    }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username = username, password= password)

        if user is None:
            messages.info(request, 'Kullanici adi veya sifre hatali, lutfen tekrar deneyin.')
            return render(request, 'login.html', context)
        
        messages.success(request, 'Basariyla giris yaptiniz.')
        login(request, user)
        return redirect('ekmekKontrol')
    user = auth.sign_in_with_email_and_password('asya_firin@ekmegimsicak.com', 'asya5580')
    return render(request,'login.html',context)
    
@login_required(login_url=('user:login'))
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız")

    return redirect('user:login')


def profil(request, id):
    user = get_object_or_404(User, id=id)
    profil = Profile.objects.filter(user=user).first()
    ekmekler = Ekmek.objects.filter(uretici = user)
    return render(request, "profile.html", {"user":user, "profil":profil, "ekmekler":ekmekler})

@login_required
def profilEdit(request, id):
    user = get_object_or_404(User, id=id)
    profile = Profile.objects.filter(user=user).first()
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if user == request.user:
        if form.is_valid():
        
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Profil başarıyla güncellendi.")

            return redirect("index")
    else:
        messages.info(request, "Başkasının profilini güncellemeye yetkiniz yok.")
        return redirect("index")
    context = {
            "form" : form
    }

    return render(request, "profileEdit.html" ,context)



def index(request):
    return render(request, "index-agency-musteri.html")

def info(request):
    return render(request, "index-agency-firin.html")


def sicakDurum(firinSonSicak):
    dakika = firinSonSicak[1]
    dakika = abs(dakika)
    degisken = 'dakika'
    if len(str(dakika)) >= 3:
        dakika = dakika//60
        degisken = 'saat'
    if firinSonSicak[1] > -10:
        firinSonSicak.append("#BA0036")
        return (str(abs(dakika)) + ' ' + degisken + ' sonra ' + firinSonSicak[0] + ' çıkıyor.')
    elif firinSonSicak[1] > -45:
        firinSonSicak.append("#ff5803")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + firinSonSicak[0] + ' çıktı.')
    else:
        firinSonSicak.append("#2861ac")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + firinSonSicak[0] + ' çıktı.')




def firinlar(request):
    keyword = request.GET.get("keyword")
    db = firebase.database()
    result = db.child("users").get().val()
    timestamp = time.time()
    for firin in result:
        firin['firinSonSicak'][1] = int((firin['firinSonSicak'][1] - timestamp) // 60)
        firin['firinSonSicak'][1] = sicakDurum(firin['firinSonSicak'])
    
    if keyword:
        for i in result:
            firinIsim = str(i['name']).lower()
            if str(keyword).lower() in firinIsim:
                context={
                    'firinlar':[i]
                }
                return render(request, "firinlar.html", context=context)
            else:
                context={
                'firinlar':result,
                }
                messages.info(request, "Maalesef aradığınız isme sahip fırın şu anda bulunmuyor :(")
                return render(request, "firinlar.html", context=context)
    context={
        'firinlar':result,
    }
    return render(request, 'firinlar.html', context=context)



def saat_renk(sonSicakObjesi):
    dakika = sonSicakObjesi[0]
    dakika = abs(dakika)
    degisken = 'dakika'
    if len(str(dakika)) >= 3:
        dakika = dakika//60
        degisken = 'saat'
    if sonSicakObjesi[0] > -10:
        sonSicakObjesi[1] = ("#BA0036")
        return (str(abs(dakika)) + ' ' + degisken + ' sonra ' + ' çıkıyor.')
    elif sonSicakObjesi[0] > -45:
        sonSicakObjesi[1] = ("#ff5803")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + ' çıktı.')
    else:
        sonSicakObjesi[1] = ("#2861ac")
        return (str(abs(dakika)) + ' ' + degisken + ' önce ' + ' çıktı.')

def detay(request, name):
    db = firebase.database()
    firin = db.child("profiles").child(name).get().val()
    suan = time.time()
    print(firin['ekmekler'])
    firin['ekmekler'] = sorted(firin['ekmekler'], key=itemgetter('sonSicak'), reverse=True)


    for ekmek in firin['ekmekler']:
        ekmek['sonSicak'] = [int((ekmek['sonSicak'] - suan) // 60), 'renk', ekmek['ekmekAdi']]
        ekmek['sonSicak'][0] = saat_renk(ekmek['sonSicak'])



    context = {
        'firin':firin
    }
    return render(request, 'detay.html', context=context)



