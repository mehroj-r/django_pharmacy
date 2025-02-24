from django.db.models import CharField

from pharmacy_app.models import Staff, Product, Category, Sale, SaleProduct, ProductPriceHistory, ProductBatch
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

class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    recorder = StaffShortSerializer(read_only=True)

    class Meta:
        model = Product
        fields= ('title', 'photo', 'category', 'recorder')

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields= ('id', 'title', 'category', 'recorder')

class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = '__all__'

class ProductShortSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields= ('title', 'category')

class SaleProductExtendedSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source="product.title")
    category = serializers.CharField(source="product.category.title")

    class Meta:
        model = SaleProduct
        fields = ('title', 'category', 'status','quantity', 'retailPrice', 'total')

class SaleExtendedSerializer(serializers.ModelSerializer):

    sale_products = SaleProductExtendedSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ('code', 'totalAmount', 'status', 'recorder', 'payment_type', 'sale_products')

class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = ('sale_id', 'code', 'totalAmount', 'status', 'recorder', 'payment_type')

class ProductPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPriceHistory
        fields = '__all__'

class ProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = '__all__'

