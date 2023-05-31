from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from pyowm import OWM
from suntime import Sun, SunTimeException
import datetime
# Create your views here.


def get_weather_info_for_home_page(city):
    owm = OWM('5bb16486eac2780614b1d9c1457c5f51')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    all_temperature = weather.temperature('celsius')
    min_temp = all_temperature['temp_min']
    max_temp = all_temperature['temp_max']
    status = weather.status
    return round(min_temp), round(max_temp), status
    
def get_weather_info_for_second_page(city):
    owm = OWM('5bb16486eac2780614b1d9c1457c5f51')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    location = observation.location
    
    latitude = location.lat
    longitude = location.lon

    all_temperature = weather.temperature('celsius')
    min_temp = all_temperature['temp_min']
    max_temp = all_temperature['temp_max']
    current_temp = all_temperature['temp']
    temp_feels_like = all_temperature['feels_like']

    status = weather.status
    humidity = weather.humidity
    wind_speed = weather.wind().get('speed')
    
    date = datetime.date.today()
    date = date.strftime('%d-%m-%Y')

    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime('%d-%m-%Y')

    day_after_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
    day_after_tomorrow_date = day_after_tomorrow.date()
    date_day = datetime.datetime.strptime(str(day_after_tomorrow_date), '%Y-%m-%d').date()
    day_of_week_after_tomorrow = date_day.strftime('%A')
    day_after_tomorrow_formatted = day_after_tomorrow.strftime('%d-%m-%Y')
    
    sun = Sun(latitude, longitude)
    abd = datetime.date.today()
    sunrise = sun.get_local_sunrise_time(abd)
    sunset= sun.get_local_sunset_time(abd)
    sunrise_formatted = sunrise.strftime('%H:%M')
    sunset_formatted = sunset.strftime('%H:%M')

    return round(min_temp), round(max_temp), round(current_temp), round(temp_feels_like), status, humidity, round(wind_speed),\
    date, tomorrow, day_of_week_after_tomorrow, day_after_tomorrow_formatted, sunrise_formatted, sunset_formatted

# def get_3_hour_info(city):
#     owm = OWM('5bb16486eac2780614b1d9c1457c5f51')
#     mgr = owm.weather_manager()

#     forecast = mgr.forecast_at_place("Berlin,DE", '3h')
#     weather_list = forecast.forecast

#     for weather in weather_list:
#         date = weather.reference_time('date').strftime('%Y-%m-%d')
#         temperature = weather.temperature(unit='celsius')
#         min_temp = temperature['temp_min']
#         max_temp = temperature['temp_max']
#         humidity = weather.humidity
#         wind_speed = weather.wind().get('speed')
#         weather_status = weather.status
#         weather_detailed_status = weather.detailed_status


def start_page(request):
    famous_locations = [
        {
            'name': 'New York',
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
        status = weather_info[4]
        status_pictures = {
            'clear' : 'clear.jpg',
            'ash' : 'ash.jpg',
            'clouds' : 'clouds.jpg',
            'drizzle' : 'drizzle.jpg',
            'dust' : 'dust.jpg',
            'fog' : 'fog.jpg',
            'haze' : 'haze.jpg',
            'mist' : 'mist.jpg',
            'rain' : 'rain.jpg',
            'sand' : 'sand.jpg',
            'smoke' : 'smoke.jpg',
            'snow' : 'snow.jpg',
            'squall' : 'squall.jpg',
            'thunderstorm' : 'thunderstorm.jpg',
            'tornado' : 'tornado.jpg'
        }
        status_image = status_pictures.get(status.lower(), 'default_image.jpg')
        data = {
            'city': location,
            'min_temp': weather_info[0],
            'max_temp': weather_info[1],
            'current_temp' : weather_info[2],
            'temp_feels_like' : weather_info[3],
            'status': status,
            'status_pic' : status_image,
            'humidity' : weather_info[5],
            'wind' : weather_info[6],
            'date' : weather_info[7],
            'tomorrow' : weather_info[8],
            'day_of_week_after_tomorrow' : weather_info[9],
            'day_after_tomorrow_formated' : weather_info[10],
            'sunrise' : weather_info[11],
            'sunset' : weather_info[12]
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
