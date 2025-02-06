from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
import json

def home(request):
    context = {}
    return render (request,'app/home.html', context)
def index (request):
    context = {}
    return render (request,'app/index.html', context)