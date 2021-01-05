from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.urls import reverse, resolve    
from crm.views import analytics, habit
from crm.models import Order, Repeats 
import json 

# Tests
# 1. For each habit, your system tracks when it has been created, and the date and time the habit tasks have been completed. 
# 2. return a list of all currently tracked habits
# 3. return a list of all habits with the same periodicity
# 4. return the longest run streak of all defined habits,
# 5. return the longest run streak for a given habit


