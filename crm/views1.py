from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from datetime import datetime, timedelta
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time
)

def home(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    dailyFilter = Order.objects.filter(interval="Daily")
    weeklyFilter = Order.objects.filter(interval="Weekly")
    context = {'orders': orders, 'total_orders': total_orders, 'dailyFilter': dailyFilter, 'weeklyFilter':weeklyFilter}
    return render(request, 'habit/dashboard.html', context)

def analytics(request):
    orders = Order.objects.all()
    total_orders = orders.count() 
    # max_strikes = len(strikeList)
    context= {'total_orders': total_orders}
    return render(request, 'habit/analytics.html', context)

def habit(request, pk): 
    testData = [{
        'habit': 'Call Mum',
        'interval': 'Weekly', 
        'date_created': '2020-09-12'
    }]
    repeats = Repeats.objects.get(id=pk)
    orders = Order.objects.all()
    order = Order.objects.get(id=pk)
    repeat = order.checkedList.filter()
    streak = order.streak
    secondToLast = order.checkedList.all().order_by('-test')
    print(secondToLast[1].test)
    penultimate = secondToLast[1].test
    lastChecked = parse_date(penultimate)
    today1 = secondToLast.first().test
    today = parse_date(today1)
    delta = today - lastChecked
    print5 = print(delta)
    order.save()
    context = {"today": today, "lastTimeStamp": lastChecked, "testData": testData, "current_streak":streak, "order":order, "repeats": repeats, "repeat": repeat}
    return render(request, 'habit/habit.html', context)



def examples(request): 
    orders = Order.objects.all()
    total_orders = orders.count() 
    context= {'total_orders': total_orders}
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
    # repeat = Repeats.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST' :
        order.delete()
        # repeat.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'habit/delete.html', context)

def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.checked += 1
        myDateCheck = datetime.today().date()
        newRep = Repeats.objects.create(test = myDateCheck)
        order.checkedList.add(newRep)
        order.test = myDateCheck
        secondToLast = order.checkedList.all().order_by('-test')
        i = 1
        j = 0
        weekly = False
        streak = 0
        latest = parse_date(secondToLast[0].test)
        previous_week = latest - timedelta(days=7)
        for oneThing in secondToLast:
            if order.interval == "Daily":
                penultimate = oneThing.test
                lastChecked = parse_date(penultimate)
                previous_day = secondToLast[i].test
                previous_day = parse_date(previous_day)
                newStreak = lastChecked - previous_day
                if newStreak.days == 1:
                    streak+=1
                if newStreak.days > 1:
                    break
                i += 1
            elif order.interval == "Weekly":
                date = parse_date(oneThing.test)
                if weekly:
                    previous_week = previous_week - timedelta(days=7)
                    weekly = False
                if not date > previous_week:
                    streak += 1
                    weekly = True
                    latest = date
                    try:
                        if (latest - parse_date(secondToLast[j + 1].test)).days > 7:
                            break
                    except:
                        pass
                j += 1
        order.streak = streak
        order.save()
        return redirect('/')


    order.save()
    return redirect('/')
    context = {'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
    return render(request, 'habit/order_form.html', context)

