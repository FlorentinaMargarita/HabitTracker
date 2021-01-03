from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Repeats)
admin.site.register(Order)
admin.site.register(Count)
# Register your models here.
