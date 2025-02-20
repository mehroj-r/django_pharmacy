from pharmacy_app.models import Staff, Product, Category, Uom, WarehouseProduct, Sale, SaleProduct, ProductPriceHistory, BackupWarehouseProduct, UomGroup
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

class StaffShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ("username", "role")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UomShortGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UomGroup
        fields = ('id','title')

class UomShortSerializer(serializers.ModelSerializer):

    uomGroup = UomShortGroupSerializer(read_only=True)

    class Meta:
        model = Uom
        fields = ('baseQuantity', 'quantity', 'uomGroup')

class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    recorder = StaffShortSerializer(read_only=True)
    uom = UomShortSerializer(read_only=True)

    class Meta:
        model = Product
        fields= ('title', 'photo', 'category', 'recorder', 'uom')

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields= ('id', 'title', 'category', 'recorder')


class UomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UomGroup
        fields = ('id', 'title')


class UomSerializer(serializers.ModelSerializer):

    uomGroup = UomGroupSerializer(read_only=True)

    class Meta:
        model = Uom
        fields = ('id', 'baseQuantity', 'quantity', 'uomGroup')


class WarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = '__all__'

class ProductPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPriceHistory
        fields = '__all__'

class BackupWarehouseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupWarehouseProduct
        fields = '__all__'

