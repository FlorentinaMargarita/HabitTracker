from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta: 
        model = Order
        fields = ['habit', 'interval']


# class CheckForm(ModelForm):
#     class Meta: 
#         model = Order
#         fields = ['checked']

