import requests
from django.shortcuts import render, redirect
from .models import CityModel
from .forms import CityForm

def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=28dd5a902028120311be7fc0569bc196'
    
    cities = CityModel.objects.order_by('-id')

    weather_data = []
    w_data=[]
    for city in cities:
        try:
            r = requests.get(url.format(city)).json()

            city_weather={
                    'id': city.id,
                    'city': city.city,
                    'temperature': r['main']['temp'],
                    'humidity': r['main']['humidity'],
                    'wind': r['wind']['speed'],
                    'description': r['weather'][0]['description'],
                    'icon': r['weather'][0]['icon'],

            }
            # (Fahrenheit - 32) * 5.0/9.0
            weather_data.append(city_weather)
            temp=(int(city_weather['temperature']) - 32) * 5/9
            data = round(temp)
            w_data.append({"id":city_weather['id'],"city":city_weather['city'],"temperature":data,"humidity":city_weather['humidity'],
            "wind":city_weather['wind'],"description":city_weather['description'],"icon":city_weather['icon']})
            print(w_data)
    
  
        except KeyError:
            city_weather={
                    'id': city.id,
                    'city': "invalid city",

            }
            w_data.append(city_weather)
           
        else:
            pass


    form = CityForm()

    context = {
        'w_data': w_data,
        'form': form
    }

    return render(request,'weather/weather.html',context)

def addcity(request):
    form = CityForm(request.POST)
    
    if form.is_valid():
        new_city = CityModel(city=request.POST['city'])
        new_city.save()

    return redirect('index')

def delete(request, city_id):
    city = CityModel.objects.get(pk=city_id)
    city.delete()

    return redirect('index')