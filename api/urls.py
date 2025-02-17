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

    path('api/create-warehouse-product/', views.WarehouseProductCreate.as_view()),
    path('api/warehouse-products/', views.ListWarehouseProducts.as_view()),
    path('api/warehouse-products/<int:product_id>/', views.WarehouseProductDetailView.as_view()),


    path('api/create-sale/', views.SaleCreate.as_view()),
    path('api/sales/', views.ListSales.as_view()),
    path('api/sales/<int:sale_id>/', views.SaleDetailView.as_view()),

    path('api/create-sale-product/', views.CreateSaleProduct.as_view()),
    path('api/sales/<int:sale_id>/products/', views.SaleProductView.as_view()),
    path('api/products/<int:product_id>/sales/', views.ProductSaleView.as_view()),
    path('api/sale-products/', views.ListSaleProducts.as_view()),
    path('api/sale-products/<int:id>/', views.SaleProductDetailView.as_view()),

    path('api/price-history/', views.ListProductPriceHistory.as_view()),
    path('api/price-history/<int:id>/', views.ProductPriceHistoryDetailView.as_view()),
    path('api/price-history/product/<int:product_id>/', views.ProductPriceHistoryByProduct.as_view()),
    path('api/price-history/recorder/<int:recorder_id>/', views.ProductPriceHistoryByRecorder.as_view()),
    path('api/price-history/product/<int:product_id>/recorder/<int:recorder_id>/', views.ProductPriceHistoryByProductByRecorder.as_view()),
    path('api/price-history/recorder/<int:recorder_id>/product/<int:product_id>/', views.ProductPriceHistoryByProductByRecorder.as_view()),

    path('api/create-warehouse-backup-product/', views.BackupWarehouseProductCreate.as_view()),
    path('api/warehouse-backup-products/', views.ListBackupWarehouseProducts.as_view()),
    path('api/warehouse-backup-products/<int:product_id>/', views.BackupWarehouseProductDetailView.as_view()),

    path('api/create-uom-group/', views.UomGroupCreate.as_view()),
    path('api/uom-groups/', views.ListUomGroups.as_view()),
    path('api/uom-groups/<int:id>/', views.UomGroupDetailView.as_view()),

]