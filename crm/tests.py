from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve    
from crm.views import analytics, habit
from crm.models import Order, Repeats 
import json 

class TestUrls(SimpleTestCase):
        def test_analytics_url_is_resolved(self): 
            url = reverse('analytics')
            print(resolve(url))
            self.assertEquals(resolve(url).func, analytics)


# I set up different things that I need, for each of the tests
class TestModels(TestCase):
    def setUp(self):
        self.order1 = Order.objects.create(
            habit='Habit1',
            interval='Weekly'
        )

 
# class TestView(TestCase):
#     # this function is going to be run before every single test method. It's used to setup a certain scenario.
#         def setUp(self):
#             self.client = Client()
#             self.analytics = reverse('analytics')
#             self.createHabit = reverse('create_habit')

# # TestCase is in the testing framework. It is from Django. Most of the testCases will inherit from TestCase by default.
# # So what is happening is the following, if we use the Django testFramework: 
# # 1.) It will run all the tests which are in the main app under the tests.py file. 
# # 2.) If the test run succesfully it will tell you "destroying test database". Here Django is creating a SQLite DB. It is putting this
# #     in memory, running everything and then destroying this database out of memory. Because it is in memory it is really fast. 
class BasicTest(TestCase):
        def test_field(self):
            habit = Order()
            habit.habit = "Write tests"
            habit.interval = "Daily"
            habit.save()

            record = Order.objects.get(pk = habit.pk)
            self.assertEqual(record, habit)

#here comes the actual test code. 

        # def test_analytics_get(self):
        #    # Here we get access to the client we setup in the setup method.   
        #     response = self.client.get(self.analytics)
        #     # here are the assertions
        #     self.assertEquals(response.status_code, 200)
        #     # This asserts that a certain response contains a specific template
        #     self.assertTemplateUsed(response, 'habit/analytics.html')

        # def test_create_habit_get(self):
        #    # Here we get access to the client we setup in the setup method.   
        #     response = self.client.get(self.createHabit)
        #     # here are the assertions
        #     self.assertEquals(response.status_code, 200)
        #     # This asserts that a certain response contains a specific template
        #     self.assertTemplateUsed(response, 'habit/order_form.html')


# Tests
# 1. For each habit, your system tracks when it has been created, and the date and time the habit tasks have been completed. 



# 2. return a list of all currently tracked habits
# 3. return a list of all habits with the same periodicity
# 4. return the longest run streak of all defined habits,
# 5. return the longest run streak for a given habit
# 6. add habit and click check

