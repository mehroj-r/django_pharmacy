from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
]