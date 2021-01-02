from django.db import models
from django.utils import timezone
from datetime import datetime, date

class Customer(models.Model):
    name = models.CharField(max_length=400, null=True)
    phone = models.CharField(max_length=400, null=True)
    email = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=400, null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
                ('Indoor', 'Indoor'),
                ('Outdoor', 'Outdoor'),
                )
    name = models.CharField(max_length=400, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=400, null=True, choices=CATEGORY)
    description = models.CharField(max_length=400, null=True, blank=True)
    date_created =  models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)


    def __str__(self):
      return self.name

class Order(models.Model): 
    INTERVAL = (
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly' ),
            ('Biweekly', 'Biweekly'),
            ('Monthly', 'Monthly'),
            )
    HABIT = (
        ('Call Mum', 'Call Mum'),
        ('Workout', 'Workout'),
        ('Buy Groceries', 'Buy Groceries'),
        ('Study Maths', 'Study Maths'),
        ('Meditate', 'Meditate'),
    )

    CHECK = (
        ('Check', 'Check'),
    )
    habit = models.CharField(max_length=200, null=True, blank=True)
    predefinedHabit = models.CharField(max_length=200, null=True, choices=HABIT, blank=True)
    interval = models.CharField(max_length=400, null=True, choices=INTERVAL)
    checked = models.IntegerField(blank=True, default=0, null=True)
    strike = models.IntegerField(blank=True, default=1, null=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False, null=True, blank=True)
    # checked = models.CharField(max_length=200, null=True, blank=True, choices=CHECK)
    # counts = models.ManyToManyField(Count)

    def __str__(self):
        return self.interval


class Count(models.Model):
    # habit = models.ForeignKey(Order)
    created = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False, null=True, blank=True)
    timeStamp = models.DateField(auto_now_add=True,  auto_now=False, blank=True)
    # updated_on = models.DateTimeField(auto_now_add=True)
    # start_time = models.DateTimeField('date published')
    # time_saved = models.DateTimeField(null=True, blank=True)
    # checked = models.IntegerField(blank=True, null=True)

    checked = models.ForeignKey(Order, null=True, default=1, on_delete=models.CASCADE)
    #  def count_total(self):

    #     return self.checked.count()



 






