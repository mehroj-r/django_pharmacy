from pharmacy_app.models import Staff, Product, Category, Uom, WarehouseProduct, Sale
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ("username", "password", "first_name", "last_name", "email", "role")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        staff = Staff(**validated_data)
        if password:
            staff.set_password(password)  # Hash password before saving
        staff.save()
        return staff

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash new password before saving
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = '__all__'


class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
