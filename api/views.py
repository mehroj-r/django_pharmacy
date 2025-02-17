from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pharmacy_app.models import Staff
from pharmacy_app.serializers import StaffSerializer, UserSerializer
from pharmacy_app.permissions import IsOwnerOrAdmin, IsOwnerOrAdmin


class StaffRegister(APIView):
    """Handles registering new users"""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StaffSerializer

    # Register a new user
    def post(self, request):

        print(request.data)

        serializer = StaffSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListStaffs(generics.ListAPIView):
    """Handles retrieving the list of all staffs"""

    permission_classes = [IsAdminUser]
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class StaffDetailView(APIView):
    """Handles retrieving, updating, deleting the staffs"""

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_staff_object(self, staff_id):
        try:
            return Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return None

    # Retrieve the user
    def get(self, request, staff_id):

        staff = self.get_staff_object(staff_id)

        if not staff:
            return Response({"error": "Staff does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update the user
    def post(self, request, staff_id):

        staff = self.get_staff_object(staff_id)

        if not staff or not staff.check_password(request.data['password']):

            return Response({"error": "Staff does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete the user
    def delete(self, request, staff_id):

        staff = self.get_staff_object(staff_id)

        if not staff:
            return Response({"error": "Staff does not exist"}, status.HTTP_404_NOT_FOUND)

        staff.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
