import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username , password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect!')
                


        context = {}
        return render(request , 'weather/login.html' , context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=022716d0515be0f4855248291306f7e3'
    
    err_msg = ''
    message = ''
    message_class = ''
   
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0 :
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Orasul nu exista!'
            else:
                err_msg= 'Orasul exista in baza de date!'
        
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Orasul a fost adaugat cu succes!'
            message_class = 'is-success'
            

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

        

    
    



    
    context = {'weather_data' : weather_data,
                'form' : form,
                'message' : message,
                'message_class' : message_class,
            }


    return render(request,'weather/weather.html',context)


def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('home')
