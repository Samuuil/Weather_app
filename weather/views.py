from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from pyowm import OWM
import datetime
from collections import Counter
# Create your views here.


def get_weather_info_for_home_page(city):
    owm = OWM('ddf4d329a74648df1a6e7d22d7050654')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    all_temperature = weather.temperature('celsius')
    min_temp = all_temperature['temp_min']
    max_temp = all_temperature['temp_max']
    status = weather.status
    return round(min_temp), round(max_temp), status    



def get_weather_info_for_second_page(city):
    owm = OWM('ddf4d329a74648df1a6e7d22d7050654')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather

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

    current_time = datetime.datetime.now()
    hour_part_now = current_time.strftime("%H")
    hour_part_now = int(hour_part_now)

    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')

    day_after_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
    day_after_tomorrow_date = day_after_tomorrow.date()
    date_day = datetime.datetime.strptime(str(day_after_tomorrow_date), '%Y-%m-%d').date()
    day_of_week_after_tomorrow = date_day.strftime('%A')
    day_after_tomorrow_formatted = day_after_tomorrow.strftime('%d-%m-%Y')

    return round(min_temp), round(max_temp), round(current_temp), round(temp_feels_like), status, humidity, round(wind_speed),\
    date, tomorrow, day_of_week_after_tomorrow, day_after_tomorrow_formatted, hour_part_now



def get_weather_forecast(city):
    owm = OWM('ddf4d329a74648df1a6e7d22d7050654')
    mgr = owm.weather_manager()
    forecast = mgr.forecast_at_place(city, '3h')
    weather_list = forecast.forecast

    weather_data = {}
    daily_status = {}

    for weather in weather_list:
        date = weather.reference_time('date').strftime('%Y-%m-%d')
        temperature = weather.temperature(unit='celsius')
        min_temp = temperature['temp_min']
        max_temp = temperature['temp_max']
        humidity = weather.humidity
        wind_speed = weather.wind().get('speed')
        status = weather.status

        if date in weather_data:
            if min_temp < weather_data[date]['min_temp']:
                weather_data[date]['min_temp'] = min_temp
            if max_temp > weather_data[date]['max_temp']:
                weather_data[date]['max_temp'] = max_temp
        else:
            weather_data[date] = {
                'min_temp': min_temp,
                'max_temp': max_temp,
                'wind_speeds': [wind_speed],
                'humidities': [humidity],
            }

        if date in daily_status:
            daily_status[date].append(status)
        else:
            daily_status[date] = [status]

        weather_data[date]['wind_speeds'].append(wind_speed)
        weather_data[date]['humidities'].append(humidity)

    weather_info = []
    for date, data in weather_data.items():
        avg_wind_speed = sum(data['wind_speeds']) / len(data['wind_speeds'])
        avg_humidity = sum(data['humidities']) / len(data['humidities'])
        most_common_status = Counter(daily_status[date]).most_common(1)[0][0]

        forecast_data = {
            'date': date,
            'min_temp': data['min_temp'],
            'max_temp': data['max_temp'],
            'wind_speed': avg_wind_speed,
            'humidity': avg_humidity,
            'most_common_status': most_common_status
        }
        
        weather_info.append(forecast_data)
    
    return weather_info

def get_weather_for_day(city):
    owm = OWM('ddf4d329a74648df1a6e7d22d7050654')
    mgr = owm.weather_manager()
    forecast = mgr.forecast_at_place(city, '3h')
    weather_list = forecast.forecast
    result = []
    counter = 0
    for weather in weather_list:
        if counter < 8:
            counter += 1
        else:
            break
        date = weather.reference_time('date').strftime('%m-%d')
        hour = weather.reference_time('date').strftime('%H:%M')
        temperature = weather.temperature(unit='celsius')
        temp = temperature['temp']
        temp_feels_like = temperature['feels_like']
        humidity = weather.humidity
        wind_speed = weather.wind().get('speed')
        status = weather.status
        pressure = weather.pressure['press']
        rain = weather.rain
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
        to_add = {
            'city' : city,
            'date' : date,
            'hour' : hour,
            'temperature' : round(temp),
            'temperature_feel_like' : round(temp_feels_like),
            'humidity' : humidity,
            'wind' : round(wind_speed),
            'status' : status_image,
            'pressure' : pressure,
            'rain' : rain
        }
        result.append(to_add)
    return result



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
        weather_forecast = get_weather_forecast(location)
        tomorrow_data = None 
        tomorrow_tomorrow_data = None
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow = str(tomorrow.strftime('%Y-%m-%d'))
        tomorrow_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
        tomorrow_tomorrow = str(tomorrow_tomorrow.strftime('%Y-%m-%d'))
        for forecast in weather_forecast:
            date = forecast['date']
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d') 
            date = str(date.date())
            if date == tomorrow:
                tomorrow_data = forecast
            if date == tomorrow_tomorrow:
                tomorrow_tomorrow_data = forecast
                break

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
            
        if tomorrow_data and tomorrow_tomorrow_data:
            tomorrow_status = tomorrow_data['most_common_status']
            status_image_tomorrow = status_pictures.get(tomorrow_status.lower(), 'default_image.jpg')
            tomorrow_tomorrow_status = tomorrow_tomorrow_data['most_common_status']
            status_image_tomorrow_tomorrow = status_pictures.get(tomorrow_tomorrow_status.lower(), 'default_image.jpg')
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
                'tomorrow_wind' : round(tomorrow_data['wind_speed']),
                'tomorrow_humidity' : round(tomorrow_data['humidity']),
                'most_common_status_tomorrow' :status_image_tomorrow,
                'tomorrow_min_temp' : round(tomorrow_data['min_temp']),
                'tomorrow_max_temp' : round(tomorrow_data['max_temp']),
                'tomorrow_tomorrow_wind' : round(tomorrow_tomorrow_data['wind_speed']),
                'tomorrow_tomorrow_humidity' : round(tomorrow_tomorrow_data['humidity']),
                'most_common_status_tomorrow_tomorrow' : status_image_tomorrow_tomorrow,
                'tomorrow_tomorrow_min_temp' : round(tomorrow_tomorrow_data['min_temp']),
                'tomorrow_tomorrow_max_temp' : round (tomorrow_tomorrow_data['max_temp']),
                'hour_part_now' : weather_info[11]
            }
            data['tomorrow_status'] = tomorrow_data['most_common_status']
            return render(request, 'current_weather.html', data)
        
    else:
        return render(request, 'start_page.html')

def hourly_forecast (request):
    if request.method == 'GET':
        location = request.GET.get('city')
        forecast_for_day = get_weather_for_day(location)
        data = {
            'city' : location,
            'forecast': forecast_for_day
        }
        return render(request, 'hourly_forecast.html', data)


def daily_forecast(request):
    return render(request, 'daily_forecast.html')

def map (request):
    city = request.GET.get('city')
    owm = OWM('ddf4d329a74648df1a6e7d22d7050654')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    location = observation.location
    latitude = round(location.lat)
    longitude = round(location.lon)
    data = {
        'lat' : latitude,
        'lon' : longitude,
        'city' : city
    }
    return render(request, 'map.html', data)


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
