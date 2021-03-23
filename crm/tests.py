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

class StreakTester():
    # the line below is the constructor for the class 
    def __init__(self, order, today):
        # self represents the instance of the class 
        self.order = order
        self.today = today
    def streak_printer(self):
            getStreaks(self.order, self.today)
            print( "\t\n" , "\t\n" ,  "\t\n","Habit Name:", self.order.habit, "\t\n" , "Date Created:", self.order.dateAsString, "\t\n" ,
            "Current Streak:",  self.order.streak, "\t\n" , "Longest Streak:" , self.order.longestStreak, 
            "\t\n", "Interval:", self.order.interval )
            for eachRepeat in self.order.checkedList.all():
                print("dates when the habit was completed: ", eachRepeat.dateAsString)

    # instead of creating a new instance of StreakTester every time I want test, I can just update the order.
    def change_order(self, order):
        self.order = order


class TestView(TestCase):
    # this function is going to be run before every single test method. It's used to setup a certain scenario.
    # Django reverse: Reverses from the name we gave to the url back to the actual url-name.
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
            all_habits = []
            daily_habits = []
            weekly_habits = []
            for order in response.context["orders"]:
                all_habits.append(order.habit)
                if order.interval == "Daily":
                    daily_habits.append(order.habit)
                if order.interval == "Weekly":
                    weekly_habits.append(order.habit)
                if order.habit == 'Read':
                    # here we make sure that the habit "read" exists. So that it doesn't pass if there is no read. 
                    foundRead = True
                    self.assertEquals(order.habit, 'Read')
                    self.assertEquals(order.checkedList.count(), 37)
                    self.assertEquals(order.longestStreak, 25)
                if order.habit == 'Prepare Meals':
                    foundPrepareMeals = True
                    self.assertEquals(order.habit, 'Prepare Meals')
                    self.assertEquals(order.checkedList.count(), 35)
                    self.assertEquals(order.longestStreak, 14)
            self.assertTrue(foundRead)
            self.assertTrue(foundPrepareMeals)
            print("\t\n", "\t\n", "\t\n", "Here is a list of all currently tracked habits: ", all_habits)
            print("\t\n", "Here are all daily habits:", daily_habits)
            print("\t\n", "Here are all weekly habits:", weekly_habits)

            # This asserts that a certain response contains a specific template
            self.assertTemplateUsed(response, 'habit/dashboard.html')

        def test_streak_test(self):
            order = Order.objects.get(habit = 'Read')
            # Today in the tests is fixed to one specific date, so that - no matter when someone runs these tests - the result makes sense. 
            # In the real application online it will calculate it according to the "real" today (aka date of today)
            today = date(2021, 2, 8)
            tester = StreakTester(order, today)
            tester.streak_printer()
            order = Order.objects.get(habit = 'Prepare Meals')
            tester.change_order(order)
            tester.streak_printer()

            order = Order.objects.get(habit = 'Organize')
            tester.change_order(order)
            tester.streak_printer()

            order = Order.objects.get(habit = 'Clean Bathroom')
            tester.change_order(order)
            tester.streak_printer()

            order = Order.objects.get(habit = 'Breathing Exercise')
            tester.change_order(order)
            tester.streak_printer()
  
            order = Order.objects.get(habit = 'Grocery Shopping')
            tester.change_order(order)
            tester.streak_printer()

        def load_data(self):
         # open is python for reading any file. With as: This remembers to close it automatically if I leave the if block. 
            with open('crm/fixtures/fixtures.json') as f:
                # load()you turning JSON encoded data into Python objects.
                fixtures = json.load(f)
                for fixture in fixtures:
                    array_with_dates = [] 
                    if fixture['model'] == 'crm.Order':
                        order = Order()
                        order.id = fixture['pk']
                        if 'habit' in fixture['fields']:
                            order.habit = fixture['fields']['habit']
                        if 'interval' in fixture['fields']:
                            order.interval = fixture['fields']['interval']
                        if 'checked' in fixture['fields']:
                            order.checked = fixture['fields']['checked']
                        if 'streak' in fixture['fields']:
                            order.streak = fixture['fields']['streak']
                        if 'longestStreak ' in fixture['fields']:
                            order.longestStreak = fixture['fields']['longestStreak']
                        if 'created' in fixture['fields']:
                            order.created = fixture['fields']['created']                                  
                        if 'timeStamp' in fixture['fields']:
                            order.timeStamp = fixture['fields']['timeStamp']
                        if 'date_created' in fixture['fields']:
                            order.date_created = fixture['fields']['date_created']
                        if 'dateAsString' in fixture['fields']:
                            order.dateAsString = fixture['fields']['dateAsString']     
                        order.save()
                        
                        if 'checkedList' in fixture['fields']:                                    
                            order.checkedList.add(*fixture['fields']['checkedList'])  
                            array_with_dates.append(fixture['fields']['checkedList'])
                        repeates_array = []
                    
                    else:
                        repeat = Repeats()
                        repeat.id = fixture['pk']
                        repeat.dateAsString = fixture['fields']['dateAsString']
                        repeat.save()
            

