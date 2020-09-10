from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ekmek.models import Ekmek
from django.http import JsonResponse
from django.utils.html import strip_tags
from .models import Profile
import json


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

    return render(request,'login.html',context)
    
@login_required(login_url=('user:login'))
def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız")

    return redirect('index')


def json1(request, id):
    #uretici = User.objects.get(id=id)
    ekmekler = Ekmek.objects.filter(uretici_id = id).values()
    ekmek_list = list(ekmekler)
    if len(ekmek_list)>0:
        for i in ekmek_list:
            i['ekmekDetayi'] = strip_tags(i['ekmekDetayi'])
            #i['ekmekResmi'] = '/media/' + i['ekmekResmi']
    return JsonResponse(ekmek_list, safe=False)


def firmalarJson(request):
    users = User.objects.all().values('id','first_name', 'last_name',)
    users_list = list(users)
    for subDict in users_list:
        subDict['ProfilePicUrl'] = Profile.objects.filter(user_id=subDict['id']).first().profilResmi.url
    users_dict = {}
    users_dict['firinlar'] = users_list
    return JsonResponse(users_dict, safe=False)


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




