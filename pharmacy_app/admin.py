from django.contrib import admin
from pharmacy_app.models import *

admin.site.register(Staff)
admin.site.register(Sale)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductPriceHistory)
admin.site.register(SaleProduct)
admin.site.register(ProductBatch)
