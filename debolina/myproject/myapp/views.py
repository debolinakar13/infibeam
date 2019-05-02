from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse

from .forms import UserCreationForm, LoginForm
from .models import User

def signup(request):

    if request.method=='POST':
        form = UserCreationForm(request.POST)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        if form.is_valid():
            user = form.save()

            email = request.POST.get('email')
            password = request.POST.get('password1')
            user = authenticate(email=email,password=password)
            get_ip = User.objects.filter(email=email).update(ip_address=ipaddress)
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form':form})

    form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

def auth_login(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return HttpResponse('<h1>Welcome')
        else:
            return render(request, 'login.html', {'form':form})
    form = LoginForm()
    return render(request, 'login.html', {'form':form})
