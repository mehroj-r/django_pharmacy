from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def sign_in(request):
    if request.POST == {}:

        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'signin.html')

    username = request.POST.get('username')
    password = request.POST.get('your_pass')

    if username == "" or password == "":
        messages.error(request, 'Please fill all the fields')
    elif User.objects.filter(username=username).exists():

        user = User.objects.get(username=username)

        if user.check_password(password):

            if hasattr(user, 'staff'):
                auth.login(request, user)
                messages.success(request, 'You are logged in')
            else:
                messages.error(request, "You can't login as a staff")
                return redirect('sign-in')

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