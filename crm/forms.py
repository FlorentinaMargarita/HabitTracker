from django.forms import ModelForm
from .models import Order
from .models import Count

class OrderForm(ModelForm):
    class Meta: 
        model = Order
        fields = ['habit', 'predefinedHabit', 'interval']


# class CheckForm(ModelForm):
#     class Meta: 
#         model = Order
#         fields = ['checked']

# class CountForm(ModelForm):
#     class Meta:
#         model = Count
#         fields = "__all__"
