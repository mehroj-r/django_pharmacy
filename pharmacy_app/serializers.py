import uuid

from django.db.models import CharField, Sum

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

class ProductLiteSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title')
    recorder = StaffShortSerializer()

    class Meta:
        model = Product
        fields = ('id', 'title', 'category_name', 'recorder')

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

    product = serializers.CharField(source='product.title', read_only=True)
    category = serializers.CharField(source='product.category.title', read_only=True)

    class Meta:
        model = SaleProduct
        fields = (
            'id', 'product', 'category', 'quantity', 'retailPrice', 'status', 'total'
        )

class SaleExtendedSerializer(serializers.ModelSerializer):

    items = SaleProductExtendedSerializer(source='sale_products', read_only=True, many=True)
    recorder = serializers.CharField(source='recorder.username', read_only=True)

    class Meta:
        model = Sale
        fields = ('code', 'totalAmount', 'status', 'recorder', 'payment_type', 'items')

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

class SaleProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleProduct
        fields = ('id', 'quantity', 'retailPrice', 'status', 'product')


class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleProductCreateSerializer(many=True)

    class Meta:
        model = Sale
        fields = ('payment_type', 'items')

    def validate(self, attrs):

        # Validate each item has sufficient stock
        items_data = attrs.get('items', [])

        for item_data in items_data:

            # Skip validation if item is not marked as SOLD
            if item_data.get('status') == SaleProduct.SaleProductStatusChoices.RETURNED:
                continue

            # Extract details
            product = item_data.get('product')
            quantity = item_data.get('quantity')
            retail_price = item_data.get('retailPrice')

            # Check stock
            stock = product.batches.filter(retailPrice=retail_price).aggregate(
                total=Sum('quantity'))['total'] or 0

            if stock < quantity:
                raise serializers.ValidationError({
                    "items": f"The sale can't be processed. Stock is not enough for product {product} at price ${retail_price}."
                })

        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Generate a unique sale code
        sale_code = f"SALE-{uuid.uuid4().hex[:4].upper()}"

        # Create the sale
        sale = Sale.objects.create(
            code=sale_code,
            recorder=self.context['request'].user,
            totalAmount=0,
            **validated_data
        )

        total = 0

        # Create the sale products
        for item_data in items_data:
            SaleProduct.objects.create(sale=sale, **item_data)
            total += item_data['retailPrice'] * item_data['quantity']

        sale.totalAmount = total
        sale.save()

        return sale