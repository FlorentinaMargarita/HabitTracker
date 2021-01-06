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
    # test1 = order.test
    test1 = repeats.test
    # parseStuff = parse_date(repeats.test.last())
    secondToLast = order.checkedList.all().order_by('-test')
    print(secondToLast)
    print(secondToLast[2].test)
    penultimate = secondToLast[2].test
    # holy = parse_date(secondToLast[2])
    # print(holy)
    print("last element", order.checkedList.first().test)
    # print1 = print(lastChecked)
    # print2 = print(today)
    # print3 = print(oneDayPassed)
    # print4 = print(delta.days)
    # print5 = print(delta1)
    # lastChecked = parse_date(test1)
    lastChecked = parse_date(test1)
    today = date.today()
    oneDayPassed = today - timedelta(days=1) 
    delta = lastChecked - oneDayPassed
    delta1 = today -  lastChecked
    print5 = print(delta)
    if today == lastChecked:
                pass
                print("1st loop runs")
    if oneDayPassed == lastChecked:
                streak += 1
                print("2nd loop runs")
    if delta.days > 1:   
            streak == 0
            print("3rd loop runs")
    # if delta.days == 
    #     streak == 0
    #     print("last loop")
    # return current_streak
    context = {"penultimate":penultimate, "compareDate": oneDayPassed, "today": today, "lastTimeStamp": lastChecked, "testData": testData, "current_streak":streak, "order":order, "repeats": repeats, "repeat": repeat}
    return render(request, 'habit/habit.html', context)

       # if timeDiff == timedelta(days=1):
    #     streak = 0
      # timeDiff = datetime.now() - timedelta(days=1)
    # delta = compareDate - entry_date
    # if delta.days == 1: # Keep the streak going!
    #             current_streak += 1
    # else: 
    #     current_streak == 0     
    # compareDate = entry_date

    # if current_streak > total_streak:
    #     total_streak = current_streak



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
    repeats = order.checkedList.count()
    if request.method == 'POST':
        order.checked += 1
        myDateCheck = date.today()    
        # myDateCheck = date.strftime("%Y-%m-%d %H:%M:%S") 
        newRep = Repeats.objects.create(test = myDateCheck)
        order.checkedList.add(newRep) 
        order.test = myDateCheck
        order.save()
        return redirect('/')
    context = {'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
    return render(request, 'habit/order_form.html', context)


    


