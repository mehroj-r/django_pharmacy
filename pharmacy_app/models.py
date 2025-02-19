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

    sale_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=120)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=SaleStatusChoices, default=SaleStatusChoices.IN_PROGRESS)

    def __str__(self):
        return self.code


class SalePayment(models.Model):

    class PaymentTypeChoices(models.TextChoices):
        CARD = "Card"
        CASH = "Cash"

    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=120)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    payment_type = models.CharField(choices=PaymentTypeChoices)

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
    photo = models.ImageField(null=True, blank=True)
    uom = models.ForeignKey(Uom, on_delete=models.SET_NULL, null=True)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class SaleProduct(models.Model):

    class SaleProductStatusChoices(models.TextChoices):
        SOLD = "Sold"
        RETURNED = "Returned"

    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=20)
    status = models.CharField(choices=SaleProductStatusChoices)

    def save(self, *args, **kwargs):

        # Handle Price Change
        if self.pk:
            old_price = self.__class__.objects.get(pk=self.pk).unitPrice
            new_price = self.unitPrice

            if old_price != new_price:
                # Record Price Change
                ProductPriceHistory.objects.create(
                    product=self.product,
                    oldPrice=old_price,
                    newPrice=new_price,
                    recorder=self.sale.recorder
                )

        # Handle product count in Warehouse
        new_status = self.status
        warehouse = self.product.warehouse

        if new_status == SaleProduct.SaleProductStatusChoices.RETURNED:
            warehouse.quantity += self.quantity # Increment if returned
        else:
            warehouse.quantity -= self.quantity # Decrement if sold

            if warehouse.quantity < 0:
                raise ValidationError("The sale can't be processed. Stock is not enough")


        super().save(*args, **kwargs)
        warehouse.save()


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

    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True, related_name="warehouse")
    quantity = models.DecimalField(decimal_places=2, max_digits=20)
    unitPrice = models.DecimalField(decimal_places=2, max_digits=20)
    recorder = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)