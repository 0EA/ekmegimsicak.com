from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import EkmekForm, Vaziyet
from django.contrib import messages
import ekmek
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from . import tasks
from pusher_push_notifications import PushNotifications
from pyfcm import FCMNotification











    