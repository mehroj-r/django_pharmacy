from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from pharmacy_app.models import Staff
from pharmacy_app.serializers import StaffSerializer

class ListUsers(generics.ListAPIView):

    permission_classes = [IsAdminUser]

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
