from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.home, name="home" ),
    path('habit/<str:pk_test>', views.habit, name="habit"),
    path('analytics/', views.analytics, name="analytics"),
    path('admin/', admin.site.urls), 
    path('create_habit/', views.createHabit, name="create_habit"),
    path('update_habit/<str:pk>', views.updateHabit, name="update_habit"),
    path('delete/<str:pk>', views.delete, name="delete"),
    path('check_habit/<int:pk>', views.checkHabit, name="check_habit")
    # path('check_habit/<str:pk>', views.checkHabit, name="check_habit")
]

    