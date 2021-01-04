from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

def home(request):
    orders = Order.objects.all()
    count = Count.objects.all()
    total_orders = orders.count()
    context = {'orders': orders, 'total_orders': total_orders}
    return render(request, 'habit/dashboard.html', context)

def analytics(request):
    orders = Order.objects.all()
    count = Count.objects.all()
    total_count = count.count()
    total_orders = orders.count() 
    context= {'total_orders': total_orders, 'total_count': total_count}
    return render(request, 'habit/analytics.html', context)

def habit(request, pk): 
    strikes = Count.objects.get(id=pk)
    repeats = Repeats.objects.filter()
    repeat = Repeats.objects.filter(id=pk)
    orders = Order.objects.all()
    order = Order.objects.get(id=pk)
    more = order.checkedList.filter()

    # orders = order.order_set.all()
    # order.count_set.all()
    order_count = orders.count()
    context = { "order":order, "order_count": order_count, "strikes":strikes, "repeats": repeats, "repeat": repeat}
    return render(request, 'habit/habit.html', context)

def count(request, pk):
    counts = Count.objects.get(all)
    checked = Repeats.objects.get(id=pk)
    total_count = counts.count()
    context = {"total_count": total_count, "checked":checked}
    return render(request, 'habit/habit.html', context)

def createHabit(request):
    form = OrderForm()
    if request.method == 'POST' :
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

# this is a functional view
# it needs to know which habit we are referring to and then it needs to save it
def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.checked += 1
        myDateCheck = datetime.now()    
        newRep = Repeats.objects.create(test = myDateCheck)
        order.checkedList.add(newRep)
        myDateCheck = datetime.now()    
        order.save()
        if order.checked % 4 == 0:
           order.strike +=1 
           Count.objects.create()
           myDateStrike = datetime.now()
           order.strikeList.add()
           order.save()
        return redirect('/')
    context = {'checked': order.checked, 'strike': order.strike, 'myDateCheck': myDateCheck, "myDateStrike": myDateStrike}
    return render(request, 'habit/order_form.html', context)



