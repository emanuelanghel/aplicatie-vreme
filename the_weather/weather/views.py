import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
             form.save()
             user = form.cleaned_data.get('username')
             messages.success(request, 'Account was created for' + user)
             return redirect('login')
    
    context = {'form':form}
    return render(request , 'weather/register.html' , context)


def loginPage(request):
    context = {}
    return render(request , 'weather/login.html' , context)

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=022716d0515be0f4855248291306f7e3'
    
    #error_msg = ''
   
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
            

    form = CityForm()

    orase = City.objects.all()

    weather_data = []

    for city in orase:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

        

    
    



    
    context = {'weather_data' : weather_data, 'form' : form}


    return render(request,'weather/weather.html',context)
