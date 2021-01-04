from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.home, name="home" ),
    path('habit/<str:pk>', views.habit, name="habit"),
    path('analytics/', views.analytics, name="analytics"),
    path('examples/', views.examples, name="examples"),
    path('examples/callMum/', views.examplesCallMum, name="examplesCallMum"),
    path('examples/workout', views.examplesWorkout, name="examplesWorkout"),
    path('examples/meditate', views.examplesMeditate, name="examplesMeditate"),
    path('examples/examplesBuyGro', views.examplesBuyGro, name="examplesBuyGro"),
    path('examples/examplesStudy', views.examplesStudy, name="examplesStudy"),
    path('admin/', admin.site.urls), 
    path('create_habit/', views.createHabit, name="create_habit"),
    path('update_habit/<str:pk>', views.updateHabit, name="update_habit"),
    path('delete/<str:pk>', views.delete, name="delete"),
    path('check_habit/<int:pk>', views.checkHabit, name="check_habit"),
]

    