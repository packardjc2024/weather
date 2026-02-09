from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import requests
from datetime import datetime, time, timedelta


def generate_zip_url(city, state):
    url = f'https://zippopotam.us/us/{state.replace(" ", "%20")}/{city}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        lat = round(float(data['places'][0]['latitude']), 2)
        long = round(float(data['places'][0]['longitude']), 2)
        return long, lat
    else:
        return 181, 91
    

def generate_forecast_url(long, lat):
    url = (
        'https://api.open-meteo.com/v1/forecast?'
        f'latitude={lat}'
        f'&longitude={long}'
        '&hourly=temperature_2m'
        '&timezone=auto'
        '&forecast_days=7'
        '&temperature_unit=fahrenheit'
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp_list = []
        num_hours = len(data['hourly']['time'])
        for i in range(num_hours):
            temp_list.append({
                'hour': data['hourly']['time'][i],
                'temp': round(data['hourly']['temperature_2m'][i])
            })
        return temp_list
    else:
        return False


def index(request):
    context = {}

    # Check if there is an error message
    if 'error_message' in request.session:
        context['error_message'] = request.session['error_message']

    # Get the most recently added 4 locations
    locations = Location.objects.all().order_by('-id')[:4]
    context['locations'] = locations

    # Get the forecast for those locations
    context['temps'] = []
    current_date = datetime.today()
    current_hour = datetime.combine(current_date, time(0, 0, 0))
    one_hour = timedelta(hours=1)

    for location in locations:
        # Create the forecast dictionary
        temp_dict = {}
        temp_dict['display_name'] = f'{location.city}, {location.state}'
        temp_dict['forecast'] = []
        days = []

        # Start with today
        date = current_hour.date()
        day = f'{date.month}/{date.day}'
        days.append(day)
        day_dict = {
            'day': day,
            'hours': []
        }

        # Get the forecast data using the open-meteo api  
        temps = generate_forecast_url(location.longitude, location.latitude)
        if not temps:
            return HttpResponse(f'something went wrong for {location.city}, {location.state}')
        
        # print(temps)
        # print(len(temps))

        for temp in temps:
            date = current_hour.date()
            day = f'{date.month}/{date.day}'
            if day not in days:
                # Reset day
                temp_dict['forecast'].append(day_dict)
                days.append(day)
                day_dict = {}
                day_dict['day'] = day
                day_dict['hours'] = []
            day_dict['hours'].append({
                    'hour': current_hour.time(),
                    'temp': temp
            })
            current_hour = current_hour + one_hour

        context['temps'].append(temp_dict)
        
        # print(context['temps'])

    # return HttpResponse(data)
    return render(request, 'home_page/index.html', context)


def search(request):
    if request.method == 'POST':
        city = request.POST.get('city').lower().strip()
        state = request.POST.get('state').lower().strip()
        long, lat = generate_zip_url(city, state)
        print(long, lat)
        if long > 180 and lat == 90:
            request.session['error_message'] = 'Unable to find location.'
        else:
            new_location = Location(
                city=city,
                state=state,
                longitude=long,
                latitude=lat
            )
            new_location.save()
            if 'error_message' in request.session:
                del request.session['error_message']
            request.session['error_message'] = None
    return redirect('home_page:index')