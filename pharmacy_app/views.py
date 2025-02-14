from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if request.POST == {}:
        return render(request, 'signin.html')

    username = request.POST.get('username')
    password = request.POST.get('your_pass')

    if username == "" or password == "":
        messages.error(request, 'Please fill all the fields')
    elif User.objects.filter(username=username).exists():

        user = User.objects.get(username=username)

        if user.check_password(password):
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid password')
    else:
        messages.error(request, 'Username does not exist')

    return render(request, 'signin.html')