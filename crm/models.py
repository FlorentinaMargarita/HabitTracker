from django.db import models
from django.utils import timezone
from datetime import datetime, date

# this class stores the time whenever a habit was repeated. This means, whenever the "did it"-button is pressed.
# Because you can't press the button several times in the same second, one habit will always have unique repeats.
	# Every entity becomes a table, every field becomes a column;
class Repeats(models.Model):
    dateAsString = models.CharField(max_length=200, null=True, blank=True)


# this is the class for habits which I named order
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
    # checkedList is a manytomany field because one habit can have many repeats. 
    # checkedlist is a join table
    checkedList = models.ManyToManyField(Repeats)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, editable=False, blank=True)
    dateAsString = models.CharField(max_length=200, null=True, blank=True)

    # the def __str__(self) function is used to display the name of the habit in the admin panel. 
    # Otherwise it would have the name Habit Object(pk), which is not so easy to work with in the database.

    def __str__(self):
                return self.habit