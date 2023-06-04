from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name = 'start_page'),
    path('current_weather/', views.current_weather, name='current_weather'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('hourly-forecast/', views.hourly_forecast, name = 'hourly_forecast'),
    path('daily-forecast/', views.daily_forecast, name = 'daily_forecast'),
    path('maps/', views.map, name = 'map'),
]