from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from datetime import datetime, timedelta

def home(request):
    orders = Order.objects.all()
    count = Count.objects.all()
    total_orders = orders.count()
    dailyFilter = Order.objects.filter(interval="Daily")
    weeklyFilter = Order.objects.filter(interval="Weekly")
    context = {'orders': orders, 'total_orders': total_orders, 'dailyFilter': dailyFilter, 'weeklyFilter':weeklyFilter}
    return render(request, 'habit/dashboard.html', context)

def analytics(request):
    orders = Order.objects.all()
    count = Count.objects.all()
    total_count = count.count()
    total_orders = orders.count() 
    # max_strikes = len(strikeList)
    context= {'total_orders': total_orders, 'total_count': total_count}
    return render(request, 'habit/analytics.html', context)

def habit(request, pk): 
    testData = [{
        'habit': 'Call Mum',
        'interval': 'Weekly', 
        'date_created': '2020-09-12'
    }]
    repeats = Repeats.objects.filter()
    orders = Order.objects.all()
    order = Order.objects.get(id=pk)
    repeat = order.checkedList.filter()
    striking = order.strikeList.filter()
    trial = Order.objects.filter(interval="Daily")
    try:
        strikes = Count.objects.get(id=pk)
    except Count.DoesNotExist:
     strikes = None
    context = { "testData": testData, "order":order, "striking":striking, "repeats": repeats, "repeat": repeat}
    return render(request, 'habit/habit.html', context)


def examples(request): 
    orders = Order.objects.all()
    count = Count.objects.all()
    total_count = count.count()
    total_orders = orders.count() 
    context= {'total_orders': total_orders, 'total_count': total_count}
    return render(request, 'habit/examples.html', context)

def examplesCallMum(request):
    testData = [{
        'habit': 'Call Mum',
        'interval': 'Weekly', 
        'date_created': '2020-09-12',
        'time_stamp1':  '2020-08-12',
        'time_stamp2':  '2020-07-12',
        'time_stamp3':  '2020-06-12',
        'time_stamp4':  '2020-05-12',
        'time_stamp5':  '2020-04-12',
        'time_stamp6':  '2020-03-12',
        'time_stamp7':  '2020-02-12',
        'time_stamp8':  '2020-01-12',
        'time_stamp9':  '2020-30-11',
        'time_stamp10': '2020-29-11',
        'time_stamp11': '2020-28-11',
        'time_stamp12': '2020-27-11',
        'time_stamp13': '2020-26-11',
        'time_stamp14': '2020-25-11',
        'time_stamp15': '2020-24-11',
        'time_stamp16': '2020-23-11',
    }]
    context = {"testData": testData}
    return render(request, 'habit/examplesCallMum.html', context)

def examplesWorkout(request):
    return render(request, 'habit/examplesWorkout.html')

def examplesMeditate(request):
    return render(request, 'habit/examplesMeditate.html')

def examplesBuyGro(request):
    return render(request, 'habit/examplesBuyGro.html')

def examplesStudy(request):
    return render(request, 'habit/examplesStudy.html')

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
    count = Count.objects.get(id=pk)
    repeat = Repeats.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST' :
        order.delete()
        count.delete()
        repeat.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'habit/delete.html', context)

# this is a functional view
# it needs to know which habit we are referring to and then it needs to save it
# def checkHabit(request, pk):
#     order = Order.objects.get(id=pk)
#     if request.method == 'POST':
#         order.checked += 1
#         date = datetime.now()    
#         myDateCheck = date.strftime("%Y-%m-%d %H:%M:%S") 
#         newRep = Repeats.objects.create(test = myDateCheck)
#         order.checkedList.add(newRep) 
#         order.save()
#         if order.checked % 4 == 0:
#            order.strike +=1 
#            myDateStrike = datetime.now()
#            formatedDate = myDateStrike.strftime("%Y-%m-%d %H:%M:%S")
#            newStrike = Count.objects.create(test = formatedDate)
#            order.strikeList.add(newStrike)
#            order.save()
#         return redirect('/')
#     context = {'checked': order.checked, 'strike': order.strike, 'myDateCheck': myDateCheck, "myDateStrike": myDateStrike}
#     return render(request, 'habit/order_form.html', context)

def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.checked += 1
        date = datetime.now()    
        myDateCheck = date.strftime("%Y-%m-%d %H:%M:%S") 
        newRep = Repeats.objects.create(test = myDateCheck)
        order.checkedList.add(newRep) 
        order.save()
        return redirect('/')
    context = {'checked': order.checked, 'myDateCheck': myDateCheck}
    return render(request, 'habit/order_form.html', context)

    def strike(request, pk): 
        order = Order.objects.get(id=pk)
        time_diff = timedelta(day=1)
        newTime = date + time_diff
        oldTime = order.timeStamp
    if newTime >= oldTime:
        strike = 0
    context = {"strike": strike}
    return render(request, 'habit/order_form.html', context)


