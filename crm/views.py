from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    total_customers = customer.count()
    total_orders = orders.count()

    # delivered = orders.filter(status='Delivered').count()
    # pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customer, 'total_customers': total_customers, 
    'total_orders': total_orders}
    return render(request, 'habit/dashboard.html', context)

def analytics(request):
    products = Product.objects.all()
    return render(request, 'habit/analytics.html', {'products':products})

def habit(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {"customer": customer, "orders":orders, "order_count": order_count}
    return render(request, 'habit/habit.html', context)
