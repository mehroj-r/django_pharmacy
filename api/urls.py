from django.urls import path
from . import views

urlpatterns = [
    path('api/list-staffs', views.ListStaffs.as_view()),
    path('api/staff/<staff_id>', views.StaffDetailView.as_view()),
    path('api/register', views.StaffRegister.as_view()),

]