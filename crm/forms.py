from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    # ModelForms interact directly with the django model fields
    class Meta: 
        model = Order
        fields = ['habit', 'interval']

