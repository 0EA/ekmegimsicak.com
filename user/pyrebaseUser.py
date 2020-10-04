import pyrebase
from django.contrib import messages
from django.shortcuts import render, redirect
config = {
  "apiKey": "AIzaSyC8sQuCoPr854RbIJlpFFrrIHUrlQecTtE",
  "authDomain": "ekmegimsicak.firebaseapp.com",
  "databaseURL": "https://ekmegimsicak.firebaseio.com/",
  "storageBucket": "ekmegimsicak.appspot.com"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


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

@girisGerekli
def logoutUser(request):
    auth.current_user = None
    messages.success(request, "Başarıyla çıkış yaptınız")
    return redirect('user:login')