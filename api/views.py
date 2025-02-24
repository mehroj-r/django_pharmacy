
from pprint import pprint
from django.db import connection
from django.db.migrations import serializer
from django.utils.timezone import override
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pharmacy_app.models import (
    Staff, Product, Category, Sale, SaleProduct, ProductPriceHistory, ProductBatch
)
from pharmacy_app.serializers import (
    StaffSerializer, ProductSerializer, CategorySerializer, ProductBatchSerializer, \
    SaleSerializer, SaleProductSerializer, ProductPriceHistorySerializer, ProductListSerializer, \
    SaleExtendedSerializer
    )
from pharmacy_app.permissions import IsOwnerOrAdmin, IsWarehouseOrAdmin


class ListCreateStaffs(generics.ListCreateAPIView):
    """Handles retrieving the list of all staffs"""

    permission_classes = [IsAuthenticated, IsAdminUser]
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
    def put(self, request, staff_id):

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


class ListCreateProducts(generics.ListCreateAPIView):
    """Handles listing all products"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(APIView):
    """Handles retrieving, updating, deleting the products"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_product_object(self, product_id):
        try:
            return Product.objects.select_related(
                'category', 'recorder'
            ).get(id=product_id)
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
    def put(self, request, product_id):

        product = self.get_product_object(product_id)

        if not product:
            return Response({"error": "Product does not exist"}, status.HTTP_404_NOT_FOUND)

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


class ListCreateCategories(generics.ListCreateAPIView):
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
    def put(self, request, category_id):

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


class ListCreateSales(generics.ListCreateAPIView):
    """Handles listing all sales"""

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]


class SaleDetailView(APIView):
    """Handles retrieving and updating individual sales"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    serializer_class = SaleExtendedSerializer

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

        serializer = SaleExtendedSerializer(sale, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a sale
    def put(self, request, sale_id):

        sale = self.get_sale_object(sale_id)

        if not sale:
            return Response({"error": "Sale does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = SaleExtendedSerializer(sale, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleProductView(APIView):
    """Retrieves SaleProducts by sale_id"""

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):

        saleproduct = SaleProduct.objects.filter(sale_id=self.kwargs['sale_id'])
        serializer = SaleProductSerializer(saleproduct, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class ProductSaleView(APIView):
    """Retrieves SaleProducts by product_id"""

    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):

        saleproduct = SaleProduct.objects.filter(product_id=self.kwargs['product_id'])
        serializer = SaleProductSerializer(saleproduct, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class ListCreateSaleProducts(generics.ListCreateAPIView):
    """Lists all the SaleProducts"""

    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer
    permission_classes = [IsAuthenticated]

class SaleProductDetailView(APIView):
    """Retrieves, updates, deletes singular SaleProduct"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    serializer_class = SaleProductSerializer

    def get_sale_product_object(self, id):

        try:
            return SaleProduct.objects.get(id=id)
        except SaleProduct.DoesNotExist:
            return None

    # Retrieves a SaleProduct
    def get(self, request, id):

        sale_product = self.get_sale_product_object(id)

        if not sale_product:
            return Response({"error": "SaleProduct does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = SaleProductSerializer(sale_product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Updates a SaleProduct
    def put(self, request, id):

        sale_product = self.get_sale_product_object(id)

        if not sale_product:
            return Response({"error": "SaleProduct does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = SaleProductSerializer(sale_product, data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a SaleProduct
    def delete(self, request, id):

        sale_product = self.get_sale_product_object(id)

        if not sale_product:
            return Response({"error": "SaleProduct does not exist"}, status.HTTP_404_NOT_FOUND)

        sale_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListProductPriceHistory(generics.ListAPIView):
    """Retrieves the list oll price changes"""

    queryset = ProductPriceHistory.objects.all()
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    serializer_class = ProductPriceHistorySerializer


class ProductPriceHistoryDetailView(APIView):
    """Retrieves, updates, deletes singular ProductPriceHistory"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]

    def get_product_price_history_object(self, id):

        try:
            return ProductPriceHistory.objects.get(id=id)
        except ProductPriceHistory.DoesNotExist:
            return None

    # Retrieves a ProductPriceHistory
    def get(self, request, id):

        product_price_history = self.get_product_price_history_object(id)

        if not product_price_history:
            return Response({"error": "ProductPriceHistory does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = ProductPriceHistorySerializer(product_price_history)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Updates a ProductPriceHistory
    def put(self, request, id):

        product_price_history = self.get_product_price_history_object(id)

        if not product_price_history:
            return Response({"error": "ProductPriceHistory does not exist"}, status.HTTP_404_NOT_FOUND)

        serializer = ProductPriceHistorySerializer(product_price_history, data=request.data, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Deletes a ProductPriceHistory
    def delete(self, request, id):

        product_price_history = self.get_product_price_history_object(id)

        if not product_price_history:
            return Response({"error": "ProductPriceHistory does not exist"}, status.HTTP_404_NOT_FOUND)

        product_price_history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductPriceHistoryByProduct(generics.ListAPIView):
    """Returns all price-history for a product"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    serializer_class = ProductPriceHistorySerializer

    @override
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        qs = ProductPriceHistory.objects.filter(product_id=product_id)
        return qs


class ProductPriceHistoryByRecorder(generics.ListAPIView):
    """Returns all price-history by recorder"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    serializer_class = ProductPriceHistorySerializer

    @override
    def get_queryset(self):
        recorder_id = self.kwargs['recorder_id']
        qs = ProductPriceHistory.objects.filter(recorder_id=recorder_id)
        return qs


class ProductPriceHistoryByProductByRecorder(generics.ListAPIView):
    """Returns all price-history for a product by a recorder"""

    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]
    serializer_class = ProductPriceHistorySerializer

    @override
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        recorder_id = self.kwargs['recorder_id']
        qs = ProductPriceHistory.objects.filter(recorder_id=recorder_id, product_id=product_id)
        return qs

class ListCreateProductBatches(generics.ListCreateAPIView):

    queryset = ProductBatch.objects.all()
    serializer_class = ProductBatchSerializer
    permission_classes = [IsAuthenticated, IsWarehouseOrAdmin]