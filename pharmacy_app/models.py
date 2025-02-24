import uuid
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.exceptions import ValidationError
from django.db import models


class Staff(AbstractUser):

    class StaffRoleChoices(models.TextChoices):
        ADMIN = "Admin"
        CASHIER = "Cashier"
        WAREHOUSE = "Warehouse"

    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(choices=StaffRoleChoices, default=StaffRoleChoices.ADMIN)

    groups = models.ManyToManyField(Group, related_name="staff_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="staff_user_permissions", blank=True)

    def save(self, *args, **kwargs):

        # Give elevated permission for 'Admin' role
        isAdmin = self.role == self.StaffRoleChoices.ADMIN
        self.is_staff = isAdmin
        self.is_superuser = isAdmin

        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name


class Sale(models.Model):

    class SaleStatusChoices(models.TextChoices):
        IN_PROGRESS = "InProgress"
        CLOSED = "Closed"

    class PaymentTypeChoices(models.TextChoices):
        CARD = "Card"
        CASH = "Cash"

    sale_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=120)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=SaleStatusChoices, default=SaleStatusChoices.IN_PROGRESS)
    payment_type = models.CharField(choices=PaymentTypeChoices, default=PaymentTypeChoices.CARD)

    def __str__(self):
        return self.code


class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Product(models.Model):

    title = models.CharField(max_length=120)
    photo = models.ImageField(null=True, blank=True)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class SaleProduct(models.Model):

    class SaleProductStatusChoices(models.TextChoices):
        SOLD = "Sold"
        RETURNED = "Returned"
        PENDING = "Pending"

    sale = models.ForeignKey(Sale, related_name='sale_products', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    retailPrice = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(choices=SaleProductStatusChoices)

    @property
    def total(self):
        return self.quantity * self.retailPrice


class ProductPriceHistory(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    oldPrice = models.DecimalField(decimal_places=2, max_digits=20)
    newPrice = models.DecimalField(decimal_places=2, max_digits=20)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)


class ProductBatch(models.Model):

    class ProductBatchSourceChoices(models.TextChoices):
        PURCHASED = "Purchased"
        RETURNED = "Returned"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="batches")
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=20)
    retailPrice = models.DecimalField(decimal_places=2, max_digits=20)
    source = models.CharField(choices=ProductBatchSourceChoices, max_length=20, default=ProductBatchSourceChoices.PURCHASED)

    arrival_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.warehouse_product.product.name} - {self.quantity} units @ ${self.unitPrice}"

    @property
    def profit_per_sale(self):
            return self.retailPrice - self.unitPrice