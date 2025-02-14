from django.urls import path
from . import views

urlpatterns = [
    path('api/list-users', views.ListUsers.as_view()),

]