from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from pyowm import OWM
# Create your views here.


def get_weather_info_for_home_page(city):
    owm = OWM('5bb16486eac2780614b1d9c1457c5f51')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    all_temperature = weather.temperature('celsius')
    min_temp = all_temperature['temp_min']
    max_temp = all_temperature['temp_max']
    status = weather.detailed_status
    return round(min_temp), round(max_temp), status
    
def get_weather_info_for_second_page(city):
    owm = OWM('5bb16486eac2780614b1d9c1457c5f51')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    all_temperature = weather.temperature('celsius')
    min_temp = all_temperature['temp_min']
    max_temp = all_temperature['temp_max']
    current_temp = all_temperature['temp']
    temp_feels_like = all_temperature['feels_like']
    status = weather.detailed_status
    return round(min_temp), round(max_temp), round(current_temp), round(temp_feels_like), status


def start_page(request):
    famous_locations = [
        {
            'name': 'Paris',
            'min_temp': None,
            'max_temp': None,
            'status': None,
        },
        {
            'name': 'London',
            'min_temp': None,
            'max_temp': None,
            'status': None,
        },
        {
            'name': 'Tokyo',
            'min_temp': None,
            'max_temp': None,
            'status': None,
        }
    ]

    for location in famous_locations:
        min_temp, max_temp, status = get_weather_info_for_home_page(location['name'])
        location['min_temp'] = f"{min_temp}°C"
        location['max_temp'] = f"{max_temp}°C"
        location['status'] = status

    data = {
        'famous_locations': famous_locations
    }

    return render(request, 'start_page.html', data)


def current_weather(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        weather_info = get_weather_info_for_second_page(location)
        data = {
            'city': location,
            'min_temp': weather_info[0],
            'max_temp': weather_info[1],
            'current_temp' : weather_info[2],
            'temp_feels_like' : weather_info[3],
            'status': weather_info[4],
        }
        return render(request, 'current_weather.html', data)
    else:
        return render(request, 'start_page.html')

def register (request):
    if request.method == 'POST':
        username = request.POST['username']
        emaill = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['confirm-password']

        if password == password_confirm:
            if User.objects.filter(email = emaill).exists():
                messages.info(request, 'Email in use')
                return redirect('register')
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username in use')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, email = emaill, password = password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username = username, email = email, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Pravish neshto greshno ddz')
            return redirect('login')
    else:
        return render(request, 'login.html')
