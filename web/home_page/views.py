from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import requests
from datetime import datetime, time, timedelta


###############################################################################
# Functions
###############################################################################

def get_lat_long(city, state):
    """
    Uses the zippoptam api to get the lat/long for an city/state combo. 
    """
    url = f'https://zippopotam.us/us/{state.replace(" ", "%20")}/{city}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        lat = round(float(data['places'][0]['latitude']), 2)
        long = round(float(data['places'][0]['longitude']), 2)
        return long, lat
    else:
        return 181, 91
    

def get_temps(long, lat, days=7, temp_unit='fahrenheit'):
    """
    Uses the lat and long parameters for the api url and access open-meteo
    for a forecast for the given amount of days and returns the json data 
    converted to a Python dict. 
    """
    url = (
        'https://api.open-meteo.com/v1/forecast?'
        f'latitude={lat}'
        f'&longitude={long}'
        '&hourly=temperature_2m'
        '&timezone=auto'
        f'&forecast_days={days}'
        f'&temperature_unit={temp_unit}'
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return
    

def save_forecast_data(location):
    """
    Processes the json data into Temperature objects for each hour and saves 
    it to the database. 
    """
    data = get_temps(location.longitude, location.latitude)
    for i in range(len(data['hourly']['temperature_2m'])):
        hour = datetime.strptime(data['hourly']['time'][i], '%Y-%m-%dT%H:%M')
        temp = round(data['hourly']['temperature_2m'][i])
        temp_obj = Temperature.objects.create(
            city=location,
            hour=hour,
            temp=temp
        )
        temp_obj.save()


def forecast_exists(location):
    """
    Checks whether a forecast already exists in the database for the given 
    start day. If so it uses that instead of making a new api request. If 
    not it calls the save_forecast_data function. If the day exists, but is 
    not the first entry it will delete the old data for that city and make 
    a new request.
    """
    today = datetime.combine(datetime.today(), time(0, 0, 0))
    temps = Temperature.objects.filter(city=location).order_by('hour')
    if temps.exists(): 
        if temps[0].hour == today:
            return True
        else:
            for temp in temps:
                temp.delete()
            return False
    else:
        return False
    

def format_temps_context(location):
    """
    Gets the forecast data from the table and formats the context dictionary 
    correctly for use in the template render.
    """
    temps = Temperature.objects.filter(city=location).order_by('hour')
    temp_dict = {
        'location': f'{location.city.title()}, {location.state.upper()}',
        'city': location.city,
        'days': [],
        }
    for i in range(0, len(temps), 24):
        hours = temps[i:i+24]
        day_dict = {
            'day': str(hours[0].hour.month) + '/' + str(hours[0].hour.day),
            'temps': [],
            'high': hours[0].temp,
            'low': hours[0].temp
        }
        for hour in hours:
            day_dict['temps'].append({
                'hour': hour.hour.strftime('%I:%M %p').lstrip('0'),
                'temp': hour.temp,
            })
            if hour.temp > day_dict['high']:
                day_dict['high'] = hour.temp
            if hour.temp < day_dict['low']:
                day_dict['low'] = hour.temp
        temp_dict['days'].append(day_dict)
    return temp_dict


###############################################################################
# Views
###############################################################################

def index(request):
    context = {}

    # Check if there is an error message
    if 'error_message' in request.session:
        context['error_message'] = request.session['error_message']

    # Get the saved locations from the database
    locations = Location.objects.all().order_by('-id')
    context['locations'] = []

    # Get the forecast starting with today.
    for location in locations:
        if not forecast_exists(location):
            save_forecast_data(location)
        context['locations'].append(format_temps_context(location))

    return render(request, 'home_page/index.html', context)


def search(request):
    """
    Uses Zippopotam to get the lat/long for the city/state combo and then creates
    and saves a location object to the database. If there are already four 
    locations in the database then the oldes location will be deleted. 
    """
    if request.method == 'POST':
        # Get the city and state from the form.
        city = request.POST.get('city').lower().strip()
        state = request.POST.get('state').lower().strip()
        # Use Zippopotam to get the Lat/Long
        long, lat = get_lat_long(city, state)
        # Verify that it is a legitimate lat/long
        if long > 180 and lat == 90:
            request.session['error_message'] = 'Unable to find location.'
        else:
            # Create a new location object and save
            new_location = Location(
                city=city,
                state=state,
                longitude=long,
                latitude=lat
            )
            new_location.save()
            # Deletes the oldest location if there are more than four
            locations = Location.objects.all().order_by('id')
            if len(locations) > 4:
                locations[0].delete()
            # Resets the error message for the sesson
            if 'error_message' in request.session:
                del request.session['error_message']
            request.session['error_message'] = None
    return redirect('home_page:index')


def delete_location(request):
    """
    Allows the user to delete a location by clicking the button.
    """
    if request.method == 'POST':
        city = request.POST.get('city_name')
        print('city location:' + city)
        location = Location.objects.get(city=city)
        location.delete()
    return redirect('home_page:index')