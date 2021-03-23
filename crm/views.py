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
    orders = Order.objects.order_by('habit')  
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
    longest_streak_array = []
    most_checks_array = {}
    for order in orders:
        # here I list all the "longeststreak" attributes into the longest_streak_array to then find the longest of all longestStreaks.
        longest_streak_array.append(order.longestStreak)
        # here I count all the instances of Repeats in checkedList for a specific habit. 
        # I use a dictionary to be able to read the name of the habit right away if necessary.
        # the update() method updates the dictionary with elements from a the key value pair that I pass as an argument here.
        most_checks_array.update({order.checkedList.count() : order.habit})
    longest_streak = max(longest_streak_array)
    #Here the longestStreak field in the entity Orders is set to longest_streak from the line above. 
    longest_streak_habits= orders.filter(longestStreak=longest_streak)

    most_checked = max(most_checks_array)
    habit_most_checked =most_checks_array.get(most_checked)
    context= {'total_orders': total_orders, 'most_checked': most_checked, 'longest_streak': longest_streak,
    "longest_streak_habits": longest_streak_habits, "habit_most_checked": habit_most_checked}
    return render(request, 'habit/analytics.html', context)

def habit(request, pk): 
    repeats = Repeats.objects.get(id=pk)
    orders = Order.objects.all()
    order = Order.objects.get(id=pk)
    repeat = order.checkedList.filter()
    streak = order.streak
    date_array = order.checkedList.all().order_by('-dateAsString')
    penultimate = date_array[1].dateAsString
    last_checked = parse_date(penultimate)
    today1 = date_array.first().dateAsString
    today = parse_date(today1)
    order.save()
    context = {"today": today, "last_checked": last_checked, "current_streak":streak, "order":order, "repeats": repeats, "repeat": repeat}
    return render(request, 'habit/habit.html', context)


def createHabit(request):
    # OrderForm class is imported from Djangos form API
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
        my_date_check = date.today()
        # the line below creates a new Repeats-object. 
        # It stores the timedate at the second of when the habit was completed (completed is called "checked" in this project.)
        new_rep = Repeats.objects.create(dateAsString = my_date_check)
        # the line below adds the new Repeapts object in the manyToManyField called checkedList on the order.object. 
        # This will later be used to compare the dates with one another.
        order.checkedList.add(new_rep)
        order.save()
        return redirect('/')

def getStreaks(order, today):
        # At first I get all the times the habit was repeated from the order.checkedList of the Order.object.  
        date_array = list(order.checkedList.all())
        # "list_of_days_since_first_repeat" saves the dates with all the dates from the very first one ever to today. 
        list_of_days_since_first_repeat = []
        # "list_of_repeat_days" saves the dates which were checked
        list_of_repeat_days = []
        # "week_habit" appends all weeks which passed since the first time anything was checked. 
        week_habit = []
        # the first week is initalized today. 
        week_habit_date = today
        # Below we get all the Repeats ever created. 
        repeats = Repeats.objects.all()
        # first_time_stamp is first set to "None" in order not to confuse the system in case there are no repeats-objects to it yet, because 
        # it hasen't been checked yet. 
        first_time_stamp = None
        # Earliest throws an exception if there are no Repeats. This is why below there is the try-except block.
        try:
            first_time_stamp = repeats.earliest('dateAsString')
        except:
            pass
        # That is done below in order to avoid none in the queryset
        if first_time_stamp : 
            # first_repeats is really just the first_time_stamp just parsed to be a date and not a string. 
            first_repeats = parse_date(first_time_stamp.dateAsString)  
            # If today is acutally todays's date then lastRepats stands for yesterday. We do this so that the current streak 
            # is not automatically 0 if you haven't pressed it today
            last_repeats = today - timedelta(days=1)
            # time_stamp_deltas gives us a timedelta-object from yesterday to the first time anything was ever checked. 
            time_stamp_deltas = last_repeats - first_repeats

            # In this the list_of_days_since_first_repeat is produced.
            for k in range(time_stamp_deltas.days + 1):
                time_stamp_day = first_repeats + timedelta(days=k)
                list_of_days_since_first_repeat.append(time_stamp_day)
            
            # I start today and walk backwards. Here I get all the weeks. Regardless if they were checked or not. 
            while week_habit_date > first_repeats:
                #  7 days are subtracted from today
                week_habit_date -= timedelta(days=7)
                # This week is not included, in order to be a streak, even if this week it wasn't checked yet.
                week_habit.append(week_habit_date)
            # Weekdays are received in reverse order.  
            week_habit.reverse()

            # date_array is an array which has all the days which were checked
            for repeat in date_array: 
                repeated_days = parse_date(repeat.dateAsString)
                list_of_repeat_days.append(repeated_days)
        # The data type "Set" gets rid of all duplicates. 
        checked_days_array = set(list_of_repeat_days)
    
        # inCheckedDays is there in order not to need exact matches. The timedelta establishes the week in the future.
        def inCheckedDays(x, checked_days):
            # x is whatever day of the week today is. 
            for i in checked_days:        
                # The line below determines whether i is contained in the week starting at x. 
                # That is determined by wheater i is on or after x and before the week after x.
                if x<=i<x + timedelta(days=7):
                    return True 
            return False

        def tryingWeekly(a, x):
                count_current_before, longest_streak_before = a
                count_current_after = count_current_before+1
                # x in this case is the same weekday of whatever weekday is "today". x will eventually take all the values of 
                # each of the current weekday in each week from today to the date of the first repeat except for this week. 
                if inCheckedDays(x, checked_days_array):
                    return (count_current_after, count_current_after if count_current_after> longest_streak_before else longest_streak_before)
                else: 
                    return (0, longest_streak_before)
                
        def tryingDaily(a, x):
            # a is a tuple
                count_current_before, longest_streak_before = a
                # if x (one date in checked_days_array) is in the checked days the current streak will be updated by 1, else it will be set to 0
                count_current_after = count_current_before+1 if x in checked_days_array else 0

                return (count_current_after, count_current_after if count_current_after> longest_streak_before else longest_streak_before)
        
        # Initial=(0,0) stands for the tuple a that is being initialized with 0,0
        result =  list(accumulate(list_of_days_since_first_repeat, tryingDaily, initial=(0,0))) if order.interval == "Daily" else list(accumulate(week_habit, tryingWeekly, initial=(0,0))) 
        # [-1] is for the last tuple. The second [] stands for either the currentStreak [0] or the longestStreak[1]. 
        # I used accumulate insted of functools reduce to help debug the result and to grasp the intermediate steps. 
        order.longestStreak = result[-1][1]
        order.streak = result[-1][0]
        order.save()