from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

def home(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    total_customers = customer.count()
    total_orders = orders.count()
    context = {'orders': orders, 'customers': customer, 'total_customers': total_customers, 
    'total_orders': total_orders}
    return render(request, 'habit/dashboard.html', context)

def analytics(request):
    orders = Order.objects.all()
    # products = Product.objects.all()
    total_orders = orders.count() 
    context= {'total_orders': total_orders}
    return render(request, 'habit/analytics.html', context)
    # return render(request, 'habit/analytics.html', {'products':products}, context)

def habit(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {"customer": customer, "orders":orders, "order_count": order_count}
    return render(request, 'habit/habit.html', context)

def createHabit(request):
    form = OrderForm()
    if request.method == 'POST' :
        print("Printing POST: ", request.POST)
        form = OrderForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')

    context = {'form': form}
    return render(request, 'habit/order_form.html', context)


def updateHabit(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST' :
        form = OrderForm(request.POST, instance=order)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'habit/order_form.html', context)

def delete(request, pk): 
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST' :
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'habit/delete.html', context)

def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST' :
        order.checked += 1
        order.save()
        form = OrderForm(request.POST, instance=order)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'habit/order_form.html', context)