from django.db import models

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
    habit = models.CharField(max_length=200, null=True, blank=True)
    predefinedHabit = models.CharField(max_length=200, null=True, choices=HABIT, blank=True)
    timeItWillTake = models.IntegerField(null=True, blank=True)
    interval = models.CharField(max_length=400, null=True, choices=INTERVAL)

    def __str__(self):
        return self.habit



