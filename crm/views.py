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
    print('today', today)
    delta = today - lastChecked
    delta1 = today -  lastChecked
    print5 = print(delta)
    if delta.days == 1:
                streak += 1
                print("1st loop runs", "streak", streak)
                order.save()
    if delta.days == 0:
                pass
                print("2nd loop runs", streak)
                order.save()
    if delta.days > 1:   
            streak == 0
            print("3rd loop runs")
            order.save()
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

# def count(request, pk):
#     counts = Count.objects.get(all)
#     checked = Repeats.objects.get(id=pk)
#     context = {"checked":checked}
#     return render(request, 'habit/habit.html', context)

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
    repeats = order.checkedList.count()
    if request.method == 'POST':
        order.checked += 1
        myDateCheck = date.today()    
        # myDateCheck = date.strftime("%Y-%m-%d %H:%M:%S") 
        newRep = Repeats.objects.create(test = myDateCheck)
        order.checkedList.add(newRep) 
        order.test = myDateCheck
        secondToLast = order.checkedList.all().order_by('-test')
        p = 1
        i = 0
      
        for oneThing in secondToLast:
            penultimate = secondToLast[p].test
            lastChecked = parse_date(penultimate)
            today1 = secondToLast[i].test
            today = parse_date(today1)
            print('today', today)
            delta = today - lastChecked
            delta1 = today -  lastChecked
            print5 = print(delta)
            # while delta.days > 1:
            #     i+=1
            if delta.days == 1:
                order.streak += 1
                p+=1
                print("i", i, "p", p)
                print("1st loop runs", "streak", order.streak)  
            # while delta.days == 0:
            if delta.days == 0:
            #             pass
                        i+=1
                        p+=1
                        print("2nd loop runs", order.streak)  
                        print("i", i, "p", p)                  
            if delta.days > 1:   
                    order.streak == 0
                    print("3rd loop runs")            
        order.save()
        return redirect('/')
    context = {'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
    return render(request, 'habit/order_form.html', context)


    


