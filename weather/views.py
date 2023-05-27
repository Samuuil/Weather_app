from django.shortcuts import render
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

    return render(request, 'start_page.html')
