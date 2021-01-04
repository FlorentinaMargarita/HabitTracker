from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve    
from crm.views import analytics, habit, count

class TestUrls(SimpleTestCase):

        def test_analytics_url_is_resolved(self): 
            url = reverse('analytics')
            print(resolve(url))
            self.assertEquals(resolve(url).func, analytics)

 