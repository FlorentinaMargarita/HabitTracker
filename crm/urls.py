from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.home, name="home" ),
    path('habit/<str:pk_test>', views.habit, name="habit"),
    path('analytics/', views.analytics, name="analytics"),
    path('admin/', admin.site.urls), 
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>', views.updateOrder, name="update_order"),
    path('delete/<str:pk>', views.delete, name="delete")
]

    