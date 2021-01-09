from django.db import models
from django.utils import timezone
from datetime import datetime, date

class Repeats(models.Model):
    dateAsString = models.CharField(max_length=200, null=True, blank=True)


class Order(models.Model): 
    INTERVAL = (
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly' ),
                      )
    habit = models.CharField(max_length=200, null=True, blank=True)
    interval = models.CharField(max_length=400, null=True, choices=INTERVAL)
    checked = models.IntegerField(blank=True, default=0, null=True)
    streak = models.IntegerField(blank=True, default=0, null=True)
    longestStreak = models.IntegerField(blank=True, default=0, null=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False, null=True, blank=True)
    checkedList = models.ManyToManyField(Repeats)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=False, blank=True)
    dateAsString = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
	        return self.habit

 






