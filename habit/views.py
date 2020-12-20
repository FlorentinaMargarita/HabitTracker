from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'habit/dashboard.html')

def habit(request):
    return render(request, 'habit/habit.html')

def analytics(request):
    return render(request, 'habit/analytics.html')

# Create your views here.
