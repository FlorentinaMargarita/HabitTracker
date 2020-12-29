from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()

    context = {'orders': orders, 'customers': customer}
    return render(request, 'habit/dashboard.html', context)

def habit(request):
    return render(request, 'habit/habit.html')

def analytics(request):
    products = Product.objects.all()
    return render(request, 'habit/analytics.html', {'products':products})

# Create your views here.
