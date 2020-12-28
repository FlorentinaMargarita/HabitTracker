from django.urls import path
from . import views


urlpatterns = [
    path('', views.home ),
    path('habit/', views.habit),
    path('analytics/', views.analytics),
]

    