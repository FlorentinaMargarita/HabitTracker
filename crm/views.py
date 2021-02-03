from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
import calendar
from datetime import datetime, timedelta, date
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time
)
from collections import OrderedDict
from itertools import takewhile, accumulate
from pprint import pprint


# here I get all the things from the database which I want to display in my dashboard.html
def home(request):
    orders = Order.objects.all()
    for order in orders:
        getStreaks(order, date.today())
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
    longestStreakArray = []
    mostChecksArray = []
    for order in orders:
        longestStreakArray.append(order.longestStreak)
        mostChecksArray.append(order.checkedList.count(), order.habit, )
        
    longest_streak = max(longestStreakArray)
    habitForLongestStreak = orders.get(longestStreak=longest_streak)

    mostChecked = max(mostChecksArray)
    habitMostChecked = mostChecksArray.get(order.habit)
    
    context= {'total_orders': total_orders, 'mostChecked': habitMostChecked, 'longest_streak': longest_streak, "habitForLongestStreak": habitForLongestStreak}
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

def checkHabit(request, pk):
    request = request
    pk = pk
    checkHabitFakeToday(date.today(), request, pk)
    return redirect('/')
    context = {"longest": order.longestStreak, 'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
    return render(request, 'habit/order_form.html', context)

def checkHabitFakeToday(today, request, pk):
    order = Order.objects.get(id=pk)
    repeats = Repeats.objects.all()
    # This gives me the first timeStamp to which the list should be compared to
    # We are sorting by date to make sure that we get the last/first date, in case the database doesn't store them in date order.

    if request.method == 'POST':
        order.checked += 1
        myDateCheck = today
        # the line below creates a new Repeatsobject. 
        # It stores the timedate at the second of when the habit was completed in terms of this project "checked"
        newRep = Repeats.objects.create(dateAsString = myDateCheck)
        # the line below adds the new Repeapts object in the manyToManyField called checkedList on the order.object. 
        # This will later be used to compare the dates with one another.
        order.checkedList.add(newRep)
        order.dateAsString = myDateCheck
        order.save()

    

def getStreaks(order, today):
        repeats = Repeats.objects.all()
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
        weekHabitDate = today

        firstTimeStamp = repeats.earliest('dateAsString').dateAsString
        print("firstTimeSTAMP", firstTimeStamp)
        firstRepeats = parse_date(firstTimeStamp)
        lastTimeStamp = order.checkedList.latest('dateAsString').dateAsString
        lastRepeats = today - timedelta(days=1)
        print("LASTtimeStamp", lastTimeStamp)
        timeStampDeltas = lastRepeats - firstRepeats
        
        for k in range(timeStampDeltas.days + 1):
            timeStampDay = firstRepeats + timedelta(days=k)
            newArray.append(timeStampDay)
        
        # We start today and walk backwards. Here we get all the weeks. Regardless if they were checked or not. 
        while weekHabitDate > firstRepeats:
            # we subtract 7 days from today
            weekHabitDate -= timedelta(days=7)
            # we append todays date. We don't include this week, in order to be a streak, even if 
            # this week it wasn't checked yet.
            weekHabit.append(weekHabitDate)
        # this is the Monday before the very first time it has been checked. will be needed for later computations of the range of what a week is. 
        # weekHabit.append(weekHabitDate)
        # We get weekdays in reverse order. And because checkedDays is a set, there is no order. There is no concept of an order. 
        weekHabit.reverse()
   

        # dateArray is an array which has all the days which were checked
        for repeat in dateArray: 
            repeatedDays = parse_date(repeat.dateAsString)
            newArray2.append(repeatedDays)
        # newnewArray2 is done to have no duplicates in order for it to be compared. OrderDicts keeps the order when you duplicate.
        newNewArray2 = list(OrderedDict.fromkeys(newArray2))
        # Sets get rid of all duplicates. 
        checkedDaysArray = set(newNewArray2)
        allDaysArray = list(newArray)

        # inCheckedDays is there so that we don't need exact matches. The timedelta establishes the week in the future.
        def inCheckedDays(x, checkedDays):
            for i in checkedDays:         
                if x<=i<x + timedelta(days=7):
                    return True 
            return False

        def tryingWeekly(a, x):
            # a is a tuple. Tuple syntax has (). A tuple itself is immutable. But the members in a tuple are still mutable
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
        