from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    return render(request, 'habit/dashboard.html')

def habit(request):
    return render(request, 'habit/habit.html')

def analytics(request):
    products = Product.objects.all()
    return render(request, 'habit/analytics.html', {'products':products})

# Create your views here.
