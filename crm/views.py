from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from datetime import datetime, timedelta, date
from django.utils.dateparse import (parse_date)
from itertools import accumulate
from pprint import pprint


# here I get all the things from the database which I want to display in my dashboard.html
def home(request):
    orders = Order.objects.all()  
    for order in orders:
        getStreaks(order, date.today()) 
    total_orders = orders.count()
    # "daily_filter" is for showing all the habits which are daily.
    daily_filter = Order.objects.filter(interval="Daily")
    #  "weekly_filter" is for showing all the habits which are weekly.
    weekly_filter = Order.objects.filter(interval="Weekly")
    # what ever is put in "context" can then be displayed in the html-templates.
    context = {'orders': orders, 'total_orders': total_orders, 'dailyFilter':daily_filter, 'weeklyFilter':weekly_filter}
    return render(request, 'habit/dashboard.html', context)

# here I get all the things from the database which I want to display in my analytics.html
def analytics(request):
    orders = Order.objects.all()
    # with order.count I count the list of all current habits
    total_orders = orders.count()   
    longestStreakArray = []
    mostChecksArray = {}
    for order in orders:
        # here I list all the "longeststreak" attributes into the longestStreakArray to then find the longest of all longestStreaks.
        longestStreakArray.append(order.longestStreak)
        # here I count all the instances of Repeats in checkedList for a specific habit. 
        # I use a dictionary to be able to read the name of the habit right away if necessary.
        mostChecksArray.update({order.checkedList.count() : order.habit})
    longest_streak = max(longestStreakArray)
    longestStreakHabits= orders.filter(longestStreak=longest_streak)

    mostChecked = max(mostChecksArray)
    habitMostChecked = mostChecksArray.get(mostChecked)
    context= {'total_orders': total_orders, 'mostChecked': mostChecked, 'longest_streak': longest_streak,
    "longestStreakHabits":  longestStreakHabits, "habitMostChecked": habitMostChecked}
    return render(request, 'habit/analytics.html', context)

def habit(request, pk): 
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
    context = {"today": today, "lastTimeStamp": lastChecked, "current_streak":streak, "order":order, "repeats": repeats, "repeat": repeat}
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
    form = OrderForm(instance=order)
    if request.method == 'POST' :
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'habit/delete.html', context)


# Whenever a habit is checked, it creates a new instance of "Repeats", which stores the dateTime as a string in the database. 
# The habit which was checked, stores this Repeats-object in the manytomany-field called "checkedList". 
def checkHabitFakeToday(request, pk):
    order = Order.objects.get(id=pk)
    repeats = Repeats.objects.all()
    if request.method == 'POST':
        myDateCheck = date.today()
        # the line below creates a new Repeats-object. 
        # It stores the timedate at the second of when the habit was completed (completed is called "checked" in this project.)
        newRep = Repeats.objects.create(dateAsString = myDateCheck)
        # the line below adds the new Repeapts object in the manyToManyField called checkedList on the order.object. 
        # This will later be used to compare the dates with one another.
        order.checkedList.add(newRep)
        order.save()
        return redirect('/')

def getStreaks(order, today):
        # At first I get all the times the habit was repeated from the order.checkedList of the Order.object.  
        dateArray = list(order.checkedList.all())
        # "listOfDaysSinceFirstRepeat" saves the dates with all the dates from the very first one ever to today. 
        listOfDaysSinceFirstRepeat = []
        # "listOfRepeatDays" saves the dates which were checked
        listOfRepeatDays = []
        # "weekHabit" appends all weeks which passed since the first time anything was checked. 
        weekHabit = []
        # the first week is initalized today. 
        weekHabitDate = today
        # Below we get all the Repeats ever created. 
        repeats = Repeats.objects.all()
        # firstTimeStamp is first set to "None" in order not to confuse the system in case there are no repeats-objects to it yet, because 
        # it hasen't been checked yet. 
        firstTimeStamp = None
        # Earliest throws an exception if there are no Repeats. This is why below there is the try-except block.
        try:
            firstTimeStamp = repeats.earliest('dateAsString')
        except:
            pass
        # That is done below in order to avoid none in the queryset
        if firstTimeStamp : 
            # firstRepeats is really just the firstTimeStamp just parsed to be a date and not a string. 
            firstRepeats = parse_date(firstTimeStamp.dateAsString)  
            # If today is acutally todays's date then lastRepats stands for yesterday. We do this so that the current streak 
            # is not automatically 0 if you haven't pressed it today
            lastRepeats = today - timedelta(days=1)
            # timestampDelta gives us a timedelta-object from yesterday to the first time anything was ever checked. 
            timeStampDeltas = lastRepeats - firstRepeats

            # In this the listOfDaysSinceFirstRepeat is produced.
            for k in range(timeStampDeltas.days + 1):
                timeStampDay = firstRepeats + timedelta(days=k)
                listOfDaysSinceFirstRepeat.append(timeStampDay)
            
            # I start today and walk backwards. Here I get all the weeks. Regardless if they were checked or not. 
            while weekHabitDate > firstRepeats:
                #  7 days are subtracted from today
                weekHabitDate -= timedelta(days=7)
                # This week is not included, in order to be a streak, even if this week it wasn't checked yet.
                weekHabit.append(weekHabitDate)
            # Weekdays are received in reverse order.  
            weekHabit.reverse()

            # dateArray is an array which has all the days which were checked
            for repeat in dateArray: 
                repeatedDays = parse_date(repeat.dateAsString)
                listOfRepeatDays.append(repeatedDays)
        # The data type "Set" gets rid of all duplicates. 
        checkedDaysArray = set(listOfRepeatDays)
    
        # inCheckedDays is there in order not to need exact matches. The timedelta establishes the week in the future.
        def inCheckedDays(x, checkedDays):
            # x is whatever day of the week today is. 
            for i in checkedDays:        
                # The line below determines whether i is contained in the week starting at x. 
                # That is determined by wheater i is on or after x and before the week after x.
                if x<=i<x + timedelta(days=7):
                    return True 
            return False

        def tryingWeekly(a, x):
                countCurrentBefore, longestStreakBefore = a
                countCurrentAfter = countCurrentBefore+1
                # x in this case is the same weekday of whatever weekday is "today". x will eventually take all the values of 
                # each of the current weekday in each week from today to the date of the first repeat except for this week. 
                if inCheckedDays(x, checkedDaysArray):
                    return (countCurrentAfter, countCurrentAfter if countCurrentAfter> longestStreakBefore else longestStreakBefore)
                else: 
                    return (0, longestStreakBefore)
                
        def tryingDaily(a, x):
            # a is a tuple
                countCurrentBefore, longestStreakBefore = a
                # if x (one date in checkedDaysArray) is in the checked days the current streak will be updated by 1, else it will be set to 0
                countCurrentAfter = countCurrentBefore+1 if x in checkedDaysArray else 0

                return (countCurrentAfter, countCurrentAfter if countCurrentAfter> longestStreakBefore else longestStreakBefore)
        
        # Initial=(0,0) stands for the tuple a that is being initialized with 0,0
        result =  list(accumulate(listOfDaysSinceFirstRepeat, tryingDaily, initial=(0,0))) if order.interval == "Daily" else list(accumulate(weekHabit, tryingWeekly, initial=(0,0))) 
        # [-1] is for the last tuple. The second [] stands for either the currentStreak [0] or the longestStreak[1]. 
        # I used accumulate insted of functools reduce to help debug the result and to grasp the intermediate steps. 
        order.longestStreak = result[-1][1]
        order.streak =  result[-1][0]
        order.save()