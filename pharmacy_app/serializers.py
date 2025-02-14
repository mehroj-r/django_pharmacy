from pharmacy_app.models import Staff
from rest_framework import serializers

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'