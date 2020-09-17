from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ekmek.models import Ekmek
from django.http import JsonResponse
from django.utils.html import strip_tags
from .models import Profile
import json
import time
import datetime


config = {
  "apiKey": "AAAA4Mbmo0I:APA91bGKs-uJQhBI9mig3XJnpuLUnQL8yoyZij9WGpR3ACtI7uHrH8RQCYVrk4DvYDLPoDE3CGrA0F8MwMI-5egC4SiTxbj2S67DzSxVagAq0JUBRjWZg-HSqRUH-8Yws34hLOQcsM3W",
  "authDomain": "ekmegimsicak.firebaseapp.com",
  "databaseURL": "https://ekmegimsicak.firebaseio.com/",
  "storageBucket": "ekmegimsicak.appspot.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

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



def filtreJson(request):
    #uretici = User.objects.get(id=id)
    ekmekler = Ekmek.objects.all().values('ekmekAdi')
    ekmek_list = list(ekmekler)
    filtreSet = set()
    for i in ekmek_list:
        filtreSet.add(i['ekmekAdi'])
    filtreList = list(filtreSet)
    return JsonResponse(filtreList, safe=False)

def firmalarJson(request):
    users = User.objects.all().values('id','first_name', 'last_name',)
    users_list = list(users)
    for subDict in users_list:
        subDict['userName'] = User.objects.filter(profile=Profile.objects.filter(user_id=subDict['id']).first()).first().username
        subDict['aciklama'] = strip_tags(Profile.objects.filter(user_id=subDict['id']).first().aciklama)
        subDict['profilResmi'] = Profile.objects.filter(user_id=subDict['id']).first().profilResmi.url
        subDict['telefonNumarasi'] = Profile.objects.filter(user_id=subDict['id']).first().telefonNumarasi
        subDict['adres'] = Profile.objects.filter(user_id=subDict['id']).first().adres
        subDict['long'] = Profile.objects.filter(user_id=subDict['id']).first().longitude
        subDict['lat'] = Profile.objects.filter(user_id=subDict['id']).first().lat
        ekmekler = Ekmek.objects.filter(uretici=get_object_or_404(User, id=subDict['id'])).values()
        ekmekler_list = list(ekmekler)
        sicaklarListe = list()

        for i in ekmekler_list:
            i['username'] = User.objects.filter(profile=Profile.objects.filter(user_id=i['uretici_id']).first()).first().username
            try:
                if i['sonSicak'] != None:
                    i['sonSicak'] = time.mktime(datetime.datetime.strptime(i['sonSicak'], "%d/%m/%Y %H:%M:%S").timetuple())
                    sicaklarListe.append([i['ekmekAdi'], i['sonSicak']])
            except:
                i['sonSicak'] = 0

            i['ekmekDetayi'] = strip_tags(i['ekmekDetayi'])
            
        subDict['ekmekler'] = ekmekler_list

        isimler = Ekmek.objects.filter(uretici=get_object_or_404(User, id=subDict['id'])).values('ekmekAdi')
        isimListesi = list(isimler)
        temizlenmisListe = list()
        for i in isimListesi:
            temizlenmisListe.append(i['ekmekAdi'])


        subDict['ekmekIsim'] = temizlenmisListe
        

        
        try:
            def sortSecond(val): 
                return val[1]
            subDict['firinSonSicak'] = sorted(sicaklarListe, key = sortSecond, reverse = True)[0]
        except:
            subDict['firinSonSicak'] = 0
        

    users_dict = {}
    users_dict['firinlar'] = users_list
    return JsonResponse(users_dict, safe=False)


def firinJson(request, id):
    users = User.objects.filter(id=id).values('id','first_name', 'last_name',)
    users_list = list(users)
    for subDict in users_list:
        subDict['userName'] = User.objects.filter(profile=Profile.objects.filter(user_id=subDict['id']).first()).first().username
        subDict['aciklama'] = strip_tags(Profile.objects.filter(user_id=subDict['id']).first().aciklama)
        subDict['telefonNumarasi'] = Profile.objects.filter(user_id=subDict['id']).first().telefonNumarasi
        subDict['profilResmi'] = Profile.objects.filter(user_id=subDict['id']).first().profilResmi.url
        subDict['adres'] = Profile.objects.filter(user_id=subDict['id']).first().adres
        subDict['long'] = Profile.objects.filter(user_id=subDict['id']).first().longitude
        subDict['lat'] = Profile.objects.filter(user_id=subDict['id']).first().lat
        ekmekler = Ekmek.objects.filter(uretici=get_object_or_404(User, id=subDict['id'])).values()
        ekmekler_list = list(ekmekler)
        sicaklarListe = list()

        for i in ekmekler_list:
            i['username'] = User.objects.filter(profile=Profile.objects.filter(user_id=i['uretici_id']).first()).first().username
            try:
                if i['sonSicak'] != None:
                    i['sonSicak'] = time.mktime(datetime.datetime.strptime(i['sonSicak'], "%d/%m/%Y %H:%M:%S").timetuple())
                    sicaklarListe.append([i['ekmekAdi'], i['sonSicak']])
            except:
                i['sonSicak'] = 0

            i['ekmekDetayi'] = strip_tags(i['ekmekDetayi'])
            
        subDict['ekmekler'] = ekmekler_list

        isimler = Ekmek.objects.filter(uretici=get_object_or_404(User, id=subDict['id'])).values('ekmekAdi')
        isimListesi = list(isimler)
        temizlenmisListe = list()
        for i in isimListesi:
            temizlenmisListe.append(i['ekmekAdi'])


        subDict['ekmekIsim'] = temizlenmisListe
        

        
        try:
            def sortSecond(val): 
                return val[1]
            subDict['firinSonSicak'] = sorted(sicaklarListe, key = sortSecond, reverse = True)[0]
        except:
            subDict['firinSonSicak'] = 0
        
    return JsonResponse(users_list[0], safe=False)


def firinlar(request):
    context={

    }
    return render(request, 'firinlar.html', context=context)



