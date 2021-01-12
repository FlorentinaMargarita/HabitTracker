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


# the checkhabit function is the most important one of this project. 
# Whenever a habit is checked, it creates a new instance of "Repeats", which stores the dateTime as a string in the database. 
# The habit which was checked, stores this Repeats-object in the manytomany field. 

def checkHabit(request, pk):
    order = Order.objects.get(id=pk)
    repeats = Repeats.objects.all()
    # This gives me the first timeStamp to which the list should be compared to
    firstTimeStamp = repeats.first().dateAsString
    firstRepeats = parse_date(firstTimeStamp)
    lastTimeStamp = order.checkedList.last().dateAsString
    lastRepeats = parse_date(lastTimeStamp)
    timeStampDeltas = lastRepeats - firstRepeats
    # for k in range(timeStampDeltas.days + 1):
    #     firstTimeStamp += 1 
    #     print(firstTimeStamp)

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
        # Here the array in which we will compare the dates to figure out streaks is created. 
        # In order to compare the dates from today on and backwards the array has to be ordered reversed. 
        # So with the latest added dates first. This is why it says order_by('-dateAsString'). The minus here reverses the string.
        dateArray = order.checkedList.all().order_by('-dateAsString')        
        # These two indexes i and j are for counting up the current streaks.
        i = 1
        j = 0
        # Here I initalize the streaks to 0, that it can count up from there. 
        streak = 0
        # Below is to get the current week
        latest = parse_date(dateArray[0].dateAsString)
        # Below is to get the previous week. 
        previous_week = latest - timedelta(days=7)
        weekly = False
        longest_weekly = False
        # the two lines below are used to later compare for the maximum streaks. 
        longest_previous_week = latest - timedelta(days=7)
        longest = order.longestStreak = 0
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
        longest_streak = 1
        current_streak = 1
        print("dateArray as String", dateArray[i].dateAsString)
        print("FirstTimeStamp", firstRepeats)
        print("LastTimeStamp", lastTimeStamp)
        # this is the list of dates the checklist Dates should compare to
        newArray = []
        newArray2 = []
        
        for k in range(timeStampDeltas.days + 1):
            timeStampDay = firstRepeats + timedelta(days=k)
            newArray.append(timeStampDay)
            print(timeStampDay, "TIMESTAMP")
        print(newArray, "newArray")
        
        for repeat in dateArray: 
            repeatedDays = parse_date(repeat.dateAsString)
            newArray2.append(repeatedDays)
        print("newArray2", newArray2 )
        # newnewArray2 is done to have no duplicates in order for it to be compared. OrderDicts keeps the order when you duplicate.
        newNewArray2 = list(OrderedDict.fromkeys(newArray2))
        print("newnewArray2", newNewArray2, "lengthNewArray", len(newArray))
        print("length newArray2", len(newNewArray2))

        # zeroOneArray will return a list of 0 and 1. 0 for when it wasnt checked 1 if it was checked. 
        # It starts at the date when it was checked for the first time.
        zeroOneArray = []
        countMax = 0
        countCurrent = 0
        for m in newArray:
            if m in newNewArray2:
                zeroOneArray.append("1")
                countMax += 1
                countCurrent += 1
            else: 
                zeroOneArray.append("0")
                countCurrent = 0
            order.longestStreak = countMax
            order.streak = countCurrent
        print("zeroOneArray", zeroOneArray)


            
        # these indexes are for finding the maximum streaks. The logic is similar to comparing for the current streaks. Just that it
        # doesnt set back to zero when the streak breaks, but stores the longest streak so far.
        ii, jj = 1, 0
        for pointInTime in dateArray:
            if order.interval == "Daily":
                penultimate = pointInTime.dateAsString
                lastChecked = parse_date(penultimate)
                try:
                    previous_day = dateArray[ii].dateAsString
                except:
                    continue
                previous_day = parse_date(previous_day)
                newStreak = lastChecked - previous_day
                if newStreak.days == 1:
                    current_streak += 1
                if newStreak.days > 1:
                    if current_streak > longest_streak:
                        longest_streak = current_streak
                        current_streak = 0
                ii += 1
            elif order.interval == "Weekly":
                date = parse_date(pointInTime.dateAsString)
                if longest_weekly:
                    longest_previous_week = longest_previous_week - timedelta(days=7)
                    longest_weekly = False
                if not date > longest_previous_week:
                    current_streak += 1
                    if current_streak > longest_streak:
                        longest_streak = current_streak
                    longest_weekly = True
                    longest_latest = date
                    try:
                        # this is an index based comparision. Like index 0 and index 1, indea 1 and index 2 and so on.
                        # It is to compare current and previous date.
                        if (longest_latest - parse_date(dateArray[jj + 1].dateAsString)).days > 7:
                            if current_streak > longest_streak:
                                longest_streak = current_streak
                                current_streak = 0
                    except:
                        if current_streak > longest_streak:
                            longest_streak = current_streak
                            current_streak = 0
                        pass
                jj += 1
        order.streak = streak
        order.longestStreak = longest_streak if longest_streak > order.longestStreak else order.longestStreak
    order.save()
    return redirect('/')
    context = {"longest": order.longest, 'checked': order.checked, 'myDateCheck': myDateCheck, "repeats": repeats}
    return render(request, 'habit/order_form.html', context)
