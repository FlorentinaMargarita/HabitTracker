from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from datetime import datetime, timedelta
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time
)

# here I get all the things from the database which I want to display in my dashboard.html
def home(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    # "dailyfilter" is for showing all the habits which are daily
    dailyFilter = Order.objects.filter(interval="Daily")
    #  "weeklyFilter" is for showing all the habits which are weekly
    weeklyFilter = Order.objects.filter(interval="Weekly")
    # what ever is put in context will then be able to be displayed in the html-templates
    context = {'orders': orders, 'total_orders': total_orders, 'dailyFilter': dailyFilter, 'weeklyFilter':weeklyFilter}
    return render(request, 'habit/dashboard.html', context)

# here I get all the things from the database which I want to display in my analytics.html
def analytics(request):
    orders = Order.objects.all()
    # with order.count I count the list of all current habits
    total_orders = orders.count()   
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
    dateArray = order.checkedList.all().order_by('-dateAsString')
    penultimate = dateArray[1].dateAsString
    lastChecked = parse_date(penultimate)
    today1 = dateArray.first().dateAsString
    today = parse_date(today1)
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


# the checkhabit function is the most important one of this project. 
# Whenever a habit is checked, it creates a new instance of "Repeats", which stores the dateTime as a string in the database. 
# The habit which was checked, stores this Repeats-object in the manytomany field. 

def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.checked += 1
        myDateCheck = datetime.today().date()
        # the line below creates a new Repeatsobject. 
        # It stores the timedate at the second of when the habit was completed in terms of this project "checked"
        newRep = Repeats.objects.create(dateAsString = myDateCheck)
        # the line below adds the new Repeapts object in the manyToManyField called checkedList on the order.object. 
        # This will later be used to compare the dates with one another.
        order.checkedList.add(newRep)
        order.dateAsString = myDateCheck
        dateArray = order.checkedList.all().order_by('-dateAsString')
        dateArray1 = int(len(order.checkedList.all().order_by('dateAsString')))-1
        i = 1
        j = 0
        longest = order.longestStreak = 0
        p = 1
        k = 0
        weekly = False
        streak = 0
        latest = parse_date(dateArray[0].dateAsString)
        previous_week = latest - timedelta(days=7)
        max_count = 0 
        prev_int = dateArray[p]
        current = dateArray[k]
        count = 0
        difference = int(current.pk) - int(prev_int.pk)
        # here I am finding the longest streak for the habits with the daily interval. However that solution doesnt work yet.
        while k < dateArray1 and order.interval == 'Daily':
            if difference == 1:
                count+=1
                k+=1
                p+=1
                print(difference, "difference", current.pk, "currentPK", prev_int, "prevInt")
            if count > max_count:
                max_count = count
                print("max_count loop", difference, "difference", current.pk, "currentPK", prev_int, "prevInt")
            else:
                count+=1
                k+=1
                p+=1
                print("else loop")
            order.longestStreak = max_count
        for pointInTime in dateArray:
            if order.interval == "Daily":
                penultimate = pointInTime.dateAsString
                lastChecked = parse_date(penultimate)
                previous_day = dateArray[i].dateAsString
                previous_day = parse_date(previous_day)
                newStreak = lastChecked - previous_day
                if newStreak.days == 1:
                    streak+=1
                if newStreak.days > 1:
                    longest =0
                    break
                i += 1
            elif order.interval == "Weekly":
                date = parse_date(pointInTime.dateAsString)
                if weekly:
                    previous_week = previous_week - timedelta(days=7)
                    weekly = False
                if not date > previous_week:
                    streak += 1
                    weekly = True
                    latest = date
                    try:
                        if (latest - parse_date(dateArray[j + 1].dateAsString)).days > 7:
                            break
                    except:
                        pass
                j += 1
        order.streak = streak
        order.save()
        return redirect('/')
    order.save()
    return redirect('/')
    context = {"longest": order.longest, 'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
    return render(request, 'habit/order_form.html', context)

