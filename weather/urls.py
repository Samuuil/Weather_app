from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name = 'start_page'),
    path('current_weather/', views.current_weather, name='current_weather'),
    path('register/', views.register, name = 'register'),
]