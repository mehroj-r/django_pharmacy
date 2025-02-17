from django.urls import path
from . import views

urlpatterns = [
    path('api/staffs/', views.ListStaffs.as_view()),
    path('api/staffs/<int:staff_id>/', views.StaffDetailView.as_view()),
    path('api/register/', views.StaffRegister.as_view()),

    path('api/products/', views.ListProducts.as_view()),
    path('api/products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('api/create-product/', views.ProductCreate.as_view()),

    path('api/create-category/', views.CategoryCreate.as_view()),
    path('api/categories/', views.ListCategories.as_view()),
    path('api/categories/<int:category_id>/', views.CategoryDetailView.as_view()),

    path('api/create-uom/', views.UomCreate.as_view()),
    path('api/uoms/', views.ListUoms.as_view()),
    path('api/uoms/<int:uom_id>/', views.UomDetailView.as_view()),

    path('api/create-warehouseproduct/', views.WarehouseProductCreate.as_view()),
    path('api/warehouseproducts/', views.ListWarehouseProducts.as_view()),
    path('api/warehouseproducts/<int:product_id>/', views.WarehouseProductDetailView.as_view()),


    path('api/create-sale/', views.SaleCreate.as_view()),
    path('api/sales/', views.ListSales.as_view()),
    path('api/sales/<int:sale_id>/', views.SaleDetailView.as_view()),

    path('api/sales/<int:sale_id>/products/', views.SaleProductView.as_view()),
    path('api/products/<int:product_id>/sales/', views.ProductSaleView.as_view()),

]