from django.urls import path
from . import views

urlpatterns = [
    path('api/staffs/', views.ListCreateStaffs.as_view()),
    path('api/staffs/<int:staff_id>/', views.StaffDetailView.as_view()),

    path('api/products/', views.ListCreateProducts.as_view()),
    path('api/products/<int:product_id>/', views.ProductDetailView.as_view()),

    path('api/categories/', views.ListCreateCategories.as_view()),
    path('api/categories/<int:category_id>/', views.CategoryDetailView.as_view()),

    path('api/sales/', views.ListCreateSales.as_view()),
    path('api/sales/<int:sale_id>/', views.SaleDetailView.as_view()),

    path('api/sales/<int:sale_id>/products/', views.SaleProductView.as_view()),
    path('api/products/<int:product_id>/sales/', views.ProductSaleView.as_view()),
    path('api/sale-products/', views.ListCreateSaleProducts.as_view()),
    path('api/sale-products/<int:id>/', views.SaleProductDetailView.as_view()),

    path('api/price-history/', views.ListProductPriceHistory.as_view()),
    path('api/price-history/<int:id>/', views.ProductPriceHistoryDetailView.as_view()),
    path('api/price-history/product/<int:product_id>/', views.ProductPriceHistoryByProduct.as_view()),
    path('api/price-history/recorder/<int:recorder_id>/', views.ProductPriceHistoryByRecorder.as_view()),
    path('api/price-history/product/<int:product_id>/recorder/<int:recorder_id>/', views.ProductPriceHistoryByProductByRecorder.as_view()),
    path('api/price-history/recorder/<int:recorder_id>/product/<int:product_id>/', views.ProductPriceHistoryByProductByRecorder.as_view()),

    path('api/product-batches/', views.ListCreateProductBatches.as_view()),

]