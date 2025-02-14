import uuid
from django.contrib.auth.models import User
from django.db import models

class Staff(models.Model):

    class StaffRoleChoices(models.IntegerChoices):
        ADMIN = 0
        CASHIER = 1
        WAREHOUSE = 2

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=120)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.IntegerField(choices=StaffRoleChoices.choices, default=StaffRoleChoices.ADMIN)

    def __str__(self):
        return self.name


class Sale(models.Model):

    class SaleStatusChoices(models.IntegerChoices):
        IN_PROGRESS = 0
        CLOSED = 1

    sale_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=120)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=SaleStatusChoices.choices, default=SaleStatusChoices.IN_PROGRESS)

    def __str__(self):
        return self.code


class SalePayment(models.Model):

    class PaymentTypeChoices(models.IntegerChoices):
        CARD = 0
        CASH = 1

    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=120)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    payment_type = models.IntegerField(choices=PaymentTypeChoices.choices)

    def __str__(self):
        return self.code


class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class UomGroup(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Uom(models.Model):
    uomGroup = models.ForeignKey(UomGroup, on_delete=models.SET_NULL, null=True)
    baseQuantity = models.DecimalField(decimal_places=2, max_digits=20)
    quantity = models.DecimalField(decimal_places=2, max_digits=20)


class Product(models.Model):

    title = models.CharField(max_length=120)
    photo = models.ImageField()
    uom = models.ForeignKey(Uom, on_delete=models.SET_NULL, null=True)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class SaleProduct(models.Model):

    class SaleProductStatusChoices(models.IntegerChoices):
        SOLD = 0
        RETURNED = 1

    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.IntegerField(choices=SaleProductStatusChoices.choices)


class ProductPriceHistory(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    oldPrice = models.DecimalField(decimal_places=2, max_digits=20)
    newPrice = models.DecimalField(decimal_places=2, max_digits=20)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)


class BackupWarehouseProduct(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=20)


class WarehouseProduct(models.Model):

    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=20)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

