from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve    
from crm.views import analytics, habit, getStreaks
from crm.models import Order, Repeats 
from pprint import pprint
import json 
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from datetime import datetime, timedelta, date

class TestUrls(SimpleTestCase):
        def test_analytics_url_is_resolved(self): 
            url = reverse('analytics')
            print(resolve(url))
            # We always have to assert otherwise the test will always pass unless it crashes.
            self.assertEquals(resolve(url).func, analytics)

# # TestCase is in the testing framework. It is from Django. Most of the testCases will inherit from TestCase by default.
# # So what is happening is the following, if we use the Django testFramework: 
# # 1.) It will run all the tests which are in the main app under the tests.py file. 
# # 2.) If the test run succesfully it will tell you "destroying test database". Here Django is creating a SQLite DB. It is putting this
# #     in memory, running everything and then destroying this database out of memory. Because it is in memory it is really fast. 

# I set up different things that I need, for each of the tests
# class TestModels(TestCase):
#     def setUp(self):
#         pass
        # self.order1 = Order.objects.create(
        #     habit='Habit1',
        #     interval='Weekly'
        # )

class TestView(TestCase):
    # this function is going to be run before every single test method. It's used to setup a certain scenario.
    # Django reverse: back from the name we gave to the url to the actual url-name
        def setUp(self):
            # methods take self as a first argument.
            self.load_data()
            self.client = Client()
            self.analytics = reverse('analytics')
            self.createHabit = reverse('create_habit')
            self.home = reverse('home')

        def test_analytics_get(self):
           # Here we get access to the client we setup in the setup method.   
            response = self.client.get(self.analytics)
            # here are the assertions
            self.assertEquals(response.status_code, 200)
            # This asserts that a certain response contains a specific template
            self.assertTemplateUsed(response, 'habit/analytics.html')

        def test_create_habit_get(self):
           # Here we get access to the client we setup in the setup method.   
            response = self.client.get(self.createHabit)
            # here are the assertions
            self.assertEquals(response.status_code, 200)
            # This asserts that a certain response contains a specific template
            self.assertTemplateUsed(response, 'habit/order_form.html')


        def test_create_home_get(self):
        # Here we get access to the client we setup in the setup method.    
            response = self.client.get(self.home)
            # here are the assertions
            self.assertEquals(response.status_code, 200)
            foundRead = False
            foundPrepareMeals = False
            for order in response.context["orders"]:
                if order.habit == 'Read':
                    # here we make sure that the habit "read" exists. So that it doesn't pass if there is no read. 
                    foundRead = True
                    self.assertEquals(order.habit, 'Read')
                    self.assertEquals(order.checkedList.count(), 33)
                    self.assertEquals(order.longestStreak, 25)
                if order.habit == 'Prepare Meals':
                    foundPrepareMeals = True
                    self.assertEquals(order.habit, 'Prepare Meals')
                    self.assertEquals(order.checkedList.count(), 30)
                    self.assertEquals(order.longestStreak, 14)
            self.assertTrue(foundRead)
            self.assertTrue(foundPrepareMeals)

            # This asserts that a certain response contains a specific template
            self.assertTemplateUsed(response, 'habit/dashboard.html')

        def test_streak_test(self):
            order = Order.objects.get(habit = 'Read')
            today = date(2021, 2, 6)
            getStreaks(order, today)
            print("Streak:", order.habit, order.streak)
            self.assertEquals(order.streak, 0)
            order = Order.objects.get(habit = 'Prepare Meals')
            getStreaks(order, today)
            print( "\t\n" , "Habit Name:", order.habit, "\t\n" , "Date Created:", order.dateAsString, "\t\n" ,
            "Current Streak:",  order.streak, "\t\n" , "Repeats Total:", order.checkedList.count(),  "\t\n" , "Longest Streak:" , order.longestStreak, 
             "\t\n", "Interval:", order.interval, "\t\n" )
            self.assertEquals(order.streak, 1)
            
        def load_data(self):
         # open is python for reading any file. With as: This remembers to close it automatically if I leave the if block. 
            with open('crm/fixtures/fixtures.json') as f:
                fixtures = json.load(f)
                for fixture in fixtures:
                    arrayWithDates = [] 
                    if fixture['model'] == 'crm.Order':
                        order = Order()
                        order.id = fixture['pk']
                        if 'habit' in fixture['fields']:
                            order.habit = fixture['fields']['habit']
                            # print(order.habit)
                        if 'interval' in fixture['fields']:
                            order.interval = fixture['fields']['interval']
                            # print("interval for this habit: ", order.interval)
                        if 'checked' in fixture['fields']:
                            order.checked = fixture['fields']['checked']
                        if 'streak' in fixture['fields']:
                            order.streak = fixture['fields']['streak']
                            # print(order.streak, "order.strek")
                        if 'longestStreak ' in fixture['fields']:
                            order.longestStreak = fixture['fields']['longestStreak']
                            # print("longest Streak for this habit: ", order.longestStreak)
                        if 'created' in fixture['fields']:
                            order.created = fixture['fields']['created']                                  
                        if 'timeStamp' in fixture['fields']:
                            order.timeStamp = fixture['fields']['timeStamp']
                        if 'date_created' in fixture['fields']:
                            order.date_created = fixture['fields']['date_created']

                        if 'dateAsString' in fixture['fields']:
                            order.dateAsString = fixture['fields']['dateAsString']     
                            # print("date created", order.dateAsString, "\t\n")
                        order.save()
                        
                        if 'checkedList' in fixture['fields']:                                    
                            order.checkedList.add(*fixture['fields']['checkedList'])  
                            arrayWithDates.append(fixture['fields']['checkedList'])
                            # print("repeats total", order.checkedList.count())
                        # print(arrayWithDates, "arrayWithDates")
                        repeatesArray = []
                        # for dateInTime in arrayWithDates:
                        #     fixture['model'] == 'crm.Repeats'
                        #     repeat = Repeats()
                        #     repeat.id = fixture['pk']
                        #     print(repeat.id, "repeat.id")
                        #     # pk = dateInTime
                        #     # repeat.id = fixture[]
                        #     repeat.dateAsString = fixture['fields']['dateAsString']
                        #     repeatesArray.append(repeat.dateAsString)
                        #     # print("repeat.dateAsString", repeat.dateAsString)
                        #     # print(dateInTime)
                        #     print("final repeat", repeatesArray)
                    
                    else:
                        repeat = Repeats()
                        repeat.id = fixture['pk']
                        repeat.dateAsString = fixture['fields']['dateAsString']
                        # print("else", repeat.dateAsString)
                        # print(repeat.id, repr(repeat.dateAsString))
                        repeat.save()
            
        
# Tests
# 1. For each habit, your system tracks when it has been created, and the date and time the habit tasks have been completed. 
# 2. return a list of all currently tracked habits
# 3. return a list of all habits with the same periodicity
# 4. return the longest run streak of all defined habits,
# 5. return the longest run streak for a given habit
# 6. add habit and click check

