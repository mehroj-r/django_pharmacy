from pprint import pprint

from django.db import connection
from django.db.migrations import serializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pharmacy_app.models import Staff, Product, Category, Uom, WarehouseProduct, Sale, SaleProduct
from pharmacy_app.serializers import StaffSerializer, ProductSerializer, CategorySerializer, UomSerializer, \
    WarehouseProductSerializer, SaleSerializer, SaleProductSerializer
from pharmacy_app.permissions import IsOwnerOrAdmin, IsWarehouseOrAdmin


class StaffRegister(APIView):
    """Handles registering new users"""

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StaffSerializer

    # Register a new staff
    def post(self, request):

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

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_staff_object(self, staff_id):
        try:
            return Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return None

    # Retrieve the staff
    def get(self, request, staff_id):

        staff = self.get_staff_object(staff_id)

        if not staff:
            return Response({"error": "Staff does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update the staff
    def post(self, request, staff_id):

        staff = self.get_staff_object(staff_id)

        if not staff or not staff.check_password(request.data['password']):

            return Response({"error": "Staff does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete the staff
    def delete(self, request, staff_id):

        staff = self.get_staff_object(staff_id)

        if not staff:
            return Response({"error": "Staff does not exist"}, status.HTTP_404_NOT_FOUND)

        staff.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductCreate(APIView):
    """Handles creating new products"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def post(self, request):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListProducts(generics.ListAPIView):
    """Handles listing all products"""

    permission_classes = [IsWarehouseOrAdmin]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(APIView):
    """Handles retrieving, updating, deleting the products"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_product_object(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    # Retrieve a product
    def get(self, request, product_id):

        product = self.get_product_object(product_id)

        if not product:
            return Response({"error": "Product does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a product
    def post(self, request, product_id):

        product = self.get_product_object(product_id)

        if not product:
            return Response({"error": "Product does not exist"}, status.HTTP_404_NOT_FOUND)

        old_price = product.c

        serializer = ProductSerializer(product, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a product
    def delete(self, request, product_id):

        product = self.get_product_object(product_id)

        if not product:
            return Response({"error": "Product does not exist"}, status.HTTP_404_NOT_FOUND)

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryCreate(APIView):
    """Handles creating new categories"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCategories(generics.ListAPIView):
    """Handles listing all categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

class CategoryDetailView(APIView):
    """Handles retrieving, updating, deleting the category"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_category_object(self, category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    # Retrieve a category
    def get(self, request, category_id):

        category = self.get_category_object(category_id)

        if not category:
            return Response({"error": "Category does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a category
    def post(self, request, category_id):

        category = self.get_category_object(category_id)

        if not category:
            return Response({"error": "Category does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a category
    def delete(self, request, category_id):

        category = self.get_category_object(category_id)

        if not category:
            return Response({"error": "Category does not exist"}, status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UomCreate(APIView):
    """Handles creating new UOMs"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def post(self, request):
        serializer = UomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUoms(generics.ListAPIView):
    """Handles listing all UOMs"""

    queryset = Uom.objects.all()
    serializer_class = UomSerializer
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]


class UomDetailView(APIView):
    """Handles retrieving, updating, and deleting a UOM"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_uom_object(self, uom_id):
        try:
            return Uom.objects.get(id=uom_id)
        except Uom.DoesNotExist:
            return None

    # Retrieve a UOM
    def get(self, request, uom_id):
        uom = self.get_uom_object(uom_id)

        if not uom:
            return Response({"error": "UOM does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UomSerializer(uom, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a UOM
    def post(self, request, uom_id):
        uom = self.get_uom_object(uom_id)

        if not uom:
            return Response({"error": "UOM does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UomSerializer(uom, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a UOM
    def delete(self, request, uom_id):
        uom = self.get_uom_object(uom_id)

        if not uom:
            return Response({"error": "UOM does not exist"}, status=status.HTTP_404_NOT_FOUND)

        uom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WarehouseProductCreate(APIView):
    """Handles creating new warehouse products"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def post(self, request):
        serializer = WarehouseProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListWarehouseProducts(generics.ListAPIView):
    """Handles listing all warehouse products"""

    queryset = WarehouseProduct.objects.all()
    serializer_class = WarehouseProductSerializer
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]


class WarehouseProductDetailView(APIView):
    """Handles retrieving, updating, and deleting warehouse products"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_warehouse_product_object(self, product_id):
        try:
            return WarehouseProduct.objects.get(id=product_id)
        except WarehouseProduct.DoesNotExist:
            return None

    # Retrieve a warehouse product
    def get(self, request, product_id):

        warehouse_product = self.get_warehouse_product_object(product_id)

        if not warehouse_product:
            return Response({"error": "WarehouseProduct does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = WarehouseProductSerializer(warehouse_product, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a warehouse product
    def post(self, request, product_id):

        warehouse_product = self.get_warehouse_product_object(product_id)

        if not warehouse_product:
            return Response({"error": "WarehouseProduct does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = WarehouseProductSerializer(warehouse_product, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a warehouse product
    def delete(self, request, product_id):

        warehouse_product = self.get_warehouse_product_object(product_id)

        if not warehouse_product:
            return Response({"error": "WarehouseProduct does not exist"}, status.HTTP_404_NOT_FOUND)

        warehouse_product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class SaleCreate(APIView):
    """Handles creating new sales"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def post(self, request):
        serializer = SaleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSales(generics.ListAPIView):
    """Handles listing all sales"""

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]


class SaleDetailView(APIView):
    """Handles retrieving and updating individual sales"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_sale_object(self, sale_id):
        try:
            return Sale.objects.get(sale_id=sale_id)
        except Sale.DoesNotExist:
            return None

    # Retrieve a sale
    def get(self, request, sale_id):

        sale = self.get_sale_object(sale_id)

        if not sale:
            return Response({"error": "Sale does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = SaleSerializer(sale, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a sale
    def post(self, request, sale_id):

        sale = self.get_sale_object(sale_id)

        if not sale:
            return Response({"error": "Sale does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = SaleSerializer(sale, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaleProductView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, *args, **kwargs):

        saleproduct = SaleProduct.objects.filter(sale_id=self.kwargs['sale_id'])
        serializer = SaleProductSerializer(saleproduct, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class ProductSaleView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, *args, **kwargs):

        saleproduct = SaleProduct.objects.filter(product_id=self.kwargs['product_id'])
        serializer = SaleProductSerializer(saleproduct, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


