from django.db import models
from django.utils import timezone
from datetime import datetime, date
from django.contrib.auth.models import UserManager


class Count(models.Model):
    date_created = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False, null=True, blank=True)
    # order = models.ForeignKey(Order, null=True, default=1, on_delete=models.CASCADE)
    timeStamp = models.DateField(auto_now_add=True,  auto_now=False, blank=True)
    test = models.CharField(max_length=200, null=True, blank=True)
    # updated_on = models.DateTimeField(auto_now_add=True)
    # start_time = models.DateTimeField('date published')
    # time_saved = models.DateTimeField(null=True, blank=True)
    # checked = models.IntegerField(blank=True, null=True)
    # habit = models.ForeignKey(Order)
    # checked = models.ForeignKey(Order, null=True, default=1, on_delete=models.CASCADE)
    #  def count_total(self):

    #     return self.checked.count()


class Repeats(models.Model):
    date_created =  models.DateTimeField(auto_now=True, null=True, editable=False, blank=True)
    # order = models.ManyToManyField(Order)
    timeStamp = models.DateField(auto_now_add=True,  auto_now=False, blank=True)
    test = models.CharField(max_length=200, null=True, blank=True)


class Order(models.Model): 
    INTERVAL = (
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly' ),
                      )
    HABIT = (
        ('Call Mum', 'Call Mum'),
        ('Workout', 'Workout'),
        ('Buy Groceries', 'Buy Groceries'),
        ('Study Maths', 'Study Maths'),
        ('Meditate', 'Meditate'),
    )
    habit = models.CharField(max_length=200, null=True, blank=True)
    predefinedHabit = models.CharField(max_length=200, null=True, choices=HABIT, blank=True)
    interval = models.CharField(max_length=400, null=True, choices=INTERVAL)
    checked = models.IntegerField(blank=True, default=0, null=True)
    strike = models.IntegerField(blank=True, default=0, null=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False, null=True, blank=True)
    strikeList = models.ManyToManyField(Count)
    checkedList = models.ManyToManyField(Repeats)
    timeStamp = models.DateField(auto_now_add=True,  auto_now=False, blank=True)
    date_created = models.DateTimeField(auto_now=True, null=True, editable=False, blank=True)



 






