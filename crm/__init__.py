# from django.test import TestCase, Client
# from django.test import SimpleTestCase
# from django.urls import reverse, resolve    
# from crm.views import home
# from crm.models import Order, Repeats 
# # from crm.models import Order, Repeats 
# # import json 

# class TestUrls(SimpleTestCase):
#         def test_analytics_url_is_resolved(self): 
#             url = reverse('analytics')
#             print(resolve(url))
#             self.assertEquals(resolve(url).func, analytics)



# # TestCase is in the testing framework. It is from Django. Most of the testCases will inherit from TestCase by default.
# # So what is happening is the following, if we use the Django testFramework: 
# # 1.) It will run all the tests which are in the main app under the tests.py file. 
# # 2.) If the test run succesfully it will tell you "destroying test database". Here Django is creating a SQLite DB. It is putting this
# #     in memory, running everything and then destroying this database out of memory. Because it is in memory it is really fast. 
# class TestModels(TestCase):
#     def setUp(self):
#         self.order1 = Order.objects.create(
#             habit='Habit1',
#             interval='Weekly'
#         )

 
# class TestView(TestCase):
#     # this function is going to be run before every single test method. It's used to setup a certain scenario.
#         def setUp(self):
#             self.client = Client()
#             self.analytics = reverse('analytics')
#             self.createHabit = reverse('create_habit')

# #here comes the actual test code. 

# class BasicTest(TestCase):
#     def test_field(self):
#         habit = Order()
#         habit.habit = "Write tests"
#         habit.interval = "Daily"
#         habit.save()

#         record = Habit.objects.get(pk=1)
#         self.assertEqual(record, habit)

#         # def test_analytics_get(self):
#         #    # Here we get access to the client we setup in the setup method.   
#         #     response = self.client.get(self.analytics)
#         #     # here are the assertions
#         #     self.assertEquals(response.status_code, 200)
#         #     # This asserts that a certain response contains a specific template
#         #     self.assertTemplateUsed(response, 'habit/analytics.html')

#         # def test_create_habit_get(pk=1):
#         #    # Here we get access to the client we setup in the setup method.   
#         #     response = self.client.get(self.createHabit)
#         #     # here are the assertions
#         #     self.assertEquals(response.status_code, 200)
#         #     # This asserts that a certain response contains a specific template
#         #     self.assertTemplateUsed(response, 'habit/order_form.html')
