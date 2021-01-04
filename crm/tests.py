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

 
class TestView(TestCase):
        def test_order_get(self):
            # this is the setup code 
            client = Client()
            # this is the actual test code 
            response = client.get(reverse('analytics'))
            # here are the assertions
            self.assertEquals(response.status_code, 200)
            # This asserts that a certain response contains a specific template
            self.assertTemplateUsed(response, 'habit/analytics.html')
