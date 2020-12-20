from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'habit/dashboard.html')

def habit(request):
    return HttpResponse('Habit Page')

def analytics(request):
    return HttpResponse('Analytics')

# Create your views here.
