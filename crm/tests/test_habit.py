from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve    
from crm.views import analytics, habit, count
from crm.models import Order, Count, Repeats 
import json 

class TestUrls(SimpleTestCase):
        def test_analytics_url_is_resolved(self): 
            url = reverse('analytics')
            print(resolve(url))
            self.assertEquals(resolve(url).func, analytics)


class TestModels(TestCase):
    def setUp(self):
        self.order1 = Order.objects.create(
            habit='Habit1',
            interval='Weekly'
        )

 
class TestView(TestCase):
    # this function is going to be run before every single test method. It's used to setup a certain scenario.
        def setUp(self):
            self.client = Client()
            self.analytics = reverse('analytics')
            self.createHabit = reverse('create_habit')

#here comes the actual test code. 

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
