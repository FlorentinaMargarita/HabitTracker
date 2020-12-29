from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.home ),
    path('habit/', views.habit),
    path('analytics/', views.analytics),
    path('admin/', admin.site.urls), 
]

    