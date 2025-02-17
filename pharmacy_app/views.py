from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from pharmacy_app.models import Staff


def sign_in(request):
    if request.POST == {}:

        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'signin.html')

    username = request.POST.get('username')
    password = request.POST.get('your_pass')

    if username == "" or password == "":
        messages.error(request, 'Please fill all the fields')
    elif Staff.objects.filter(username=username).exists():

        user = Staff.objects.get(username=username)

        if user.check_password(password):

            auth.login(request, user)
            messages.success(request, 'You are logged in')

            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Username does not exist')

    return redirect('sign-in')

def logout(request):

    auth.logout(request)

    return redirect('sign-in')

def index(request):
    return redirect('sign-in')

def home(request):

    user = request.user

    if user.is_authenticated:
        return render(request, 'home.html', {"user": user})

    return redirect('sign-in')