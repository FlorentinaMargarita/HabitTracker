from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
import calendar
from datetime import datetime, timedelta
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time
)
from collections import OrderedDict
from itertools import takewhile, accumulate
from pprint import pprint


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
    if request.method == 'POST':
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


# the checkHabitFakeToday function is the most important one of this project. It uses a fake date for today, so that the pytests
# can be run, without starting the database. 
# Whenever a habit is checked, it creates a new instance of "Repeats", which stores the dateTime as a string in the database. 
# The habit which was checked, stores this Repeats-object in the manytomany field. 

# All that the checkHabit does is to call the actual checkhabitFakeToday function and pass it the real date of today as an argument.
# This way the tests can be run and the web application work, and the date of today won't confuse the outcomes.

#@S: I keep getting this error: The view crm.views.checkHabit didn't return an HttpResponse object. It returned None instead.
# def checkHabit(request, pk):
#     request = request
#     pk = pk
#     checkHabitFakeToday(date.today(), request, pk)
#     print(request, "request")
#     print(pk, "PK")

# @S: this is what I tried and what didn't work
# def checkHabitFakeToday(today, request, pk):
def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    repeats = Repeats.objects.all()
    # This gives me the first timeStamp to which the list should be compared to
    # We are sorting by date to make sure that we get the last/first date, in case the database doesn't store them in date order.

    if request.method == 'POST':
        order.checked += 1
        myDateCheck = datetime.today().date()
        # the line below creates a new Repeatsobject. 
        # It stores the timedate at the second of when the habit was completed in terms of this project "checked"
        newRep = Repeats.objects.create(dateAsString = myDateCheck)
        # the line below adds the new Repeapts object in the manyToManyField called checkedList on the order.object. 
        # This will later be used to compare the dates with one another.
        order.checkedList.add(newRep)
        order.save()
        order.dateAsString = myDateCheck
        # Here the array in which we will compare the dates to figure out streaks is created. 
        # In order to compare the dates from today on and backwards the array has to be ordered reversed. 
        # So with the latest added dates first. This is why it says order_by('-dateAsString'). The minus reverses the string.
        dateArray = order.checkedList.all().order_by('-dateAsString')
        # Here I initalize the streaks to 0, that it can count up from there. 
        streak = 0
        # this is the list of dates the checklist Dates should compare to
        # "newArray" saves the dates with all the dates from the very first one ever to today
        newArray = []
        # "newArray2" saves the dates which where checked
        newArray2 = []
        weekHabit = []
        weekHabitDate = date.today()

        firstTimeStamp = repeats.earliest('dateAsString').dateAsString
        firstRepeats = parse_date(firstTimeStamp)
        lastTimeStamp = order.checkedList.latest('dateAsString').dateAsString
        lastRepeats = parse_date(lastTimeStamp)
        timeStampDeltas = lastRepeats - firstRepeats
        
        for k in range(timeStampDeltas.days + 1):
            timeStampDay = firstRepeats + timedelta(days=k)
            newArray.append(timeStampDay)
        
        # We start today and walk backwards. Here we get all the weeks. Regardless if they were checked or not. 
        while weekHabitDate > firstRepeats:
            # we append todays date
            weekHabit.append(weekHabitDate)
            # we subtract 7 days from today
            weekHabitDate -= timedelta(days=7)
        # this is the Monday before the very first time it has been checked. will be needed for later computations of the range of what a week is. 
        weekHabit.append(weekHabitDate)
        # We get weekdays in reverse order. And because checkedDays is a set, there is no order. There is no concept of an order. 
        weekHabit.reverse()
   

        # dateArray is an array which has all the days which were checked
        for repeat in dateArray: 
            repeatedDays = parse_date(repeat.dateAsString)
            newArray2.append(repeatedDays)
        # newnewArray2 is done to have no duplicates in order for it to be compared. OrderDicts keeps the order when you duplicate.
        newNewArray2 = list(OrderedDict.fromkeys(newArray2))
        checkedDaysArray = set(newNewArray2)
        allDaysArray = list(newArray)

        # inCheckedDays is there so that we don't need exact matches. The timedelta establishes the week in the future.
        def inCheckedDays(x, checkedDays):
            for i in checkedDays:         
                if x<=i<x + timedelta(days=7):
                    return True 
            return False

        def tryingWeekly(a, x):
            # a is a tuple. Tuple syntax has ()
            if order.interval == "Weekly":
                countCurrentBefore, longestStreakBefore = a
                countCurrentAfter = countCurrentBefore+1    
                if inCheckedDays(x,  checkedDaysArray):
                    return (countCurrentAfter, countCurrentAfter if countCurrentAfter> longestStreakBefore else longestStreakBefore)
                else: 
                    return (0, longestStreakBefore)
                
    
        def tryingDaily(a, x):
            # a is a tuple
            if order.interval == "Daily":
                countCurrentBefore, longestStreakBefore = a
                countCurrentAfter = countCurrentBefore+1 if x in checkedDaysArray else 0

                return (countCurrentAfter, countCurrentAfter if countCurrentAfter> longestStreakBefore else longestStreakBefore)
        
        result =  list(accumulate(allDaysArray, tryingDaily, initial=(0,0))) if order.interval == "Daily" else list(accumulate(weekHabit, tryingWeekly, initial=(0,0)))
    
        
        # [-1]is for the last tuple, second value which is longest streak  
        order.longestStreak = result[-1][1]
        order.streak =  result[-1][0]
    
        order.save()
        return redirect('/')
        context = {"longest": order.longestStreak, 'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
        return render(request, 'habit/order_form.html', context)
