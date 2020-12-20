from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse('Home Page')

def habit(request):
    return HttpResponse('Habit Page')

def analytics(request):
    return HttpResponse('Analytics')

# Create your views here.
