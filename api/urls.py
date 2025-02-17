from django.urls import path
from . import views

urlpatterns = [
    path('api/list-staffs', views.ListStaffs.as_view()),
    path('api/staff/<staff_id>', views.StaffDetailView.as_view()),
    path('api/register', views.StaffRegister.as_view()),

    path('api/list-products', views.ListProducts.as_view()),
    path('api/product/<product_id>', views.ProductDetailView.as_view()),
    path('api/create-product', views.ProductCreate.as_view()),

    path('api/create-category', views.CategoryCreate.as_view()),
    path('api/list-categories', views.ListCategories.as_view()),
    path('api/category/<category_id>', views.CategoryDetailView.as_view()),

    path('api/create-uom', views.UomCreate.as_view()),
    path('api/list-uoms', views.ListUoms.as_view()),
    path('api/uom/<uom_id>', views.UomDetailView.as_view()),

    path('api/create-warehouseproduct', views.WarehouseProductCreate.as_view()),
    path('api/list-warehouseproducts', views.ListWarehouseProducts.as_view()),
    path('api/warehouseproduct/<product_id>', views.WarehouseProductDetailView.as_view()),


    path('api/create-sale', views.SaleCreate.as_view()),
    path('api/list-sales', views.ListSales.as_view()),
    path('api/sale/<sale_id>', views.SaleDetailView.as_view()),

]