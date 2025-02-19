from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import SaleProduct, ProductPriceHistory

@receiver(pre_save, sender=SaleProduct)
def handle_price_change(sender, instance, **kwargs):
    """Detect price change before saving"""

    if instance.pk:  # Only check updating, not creating
        old_instance = sender.objects.get(pk=instance.pk)

        if old_instance.unitPrice != instance.unitPrice:

            ProductPriceHistory.objects.create(
                product=instance.product,
                oldPrice=old_instance.unitPrice,
                newPrice=instance.unitPrice,
                recorder=instance.sale.recorder
            )

@receiver(pre_save, sender=SaleProduct)
def validate_stock(sender, instance, **kwargs):
    """Ensure enough stock before saving"""
    warehouse = instance.product.warehouse

    if instance.status == SaleProduct.SaleProductStatusChoices.SOLD and warehouse.quantity < instance.quantity:
        raise ValidationError("The sale can't be processed. Stock is not enough")

@receiver(post_save, sender=SaleProduct)
def update_warehouse_stock(sender, instance, created, **kwargs):
    """Update warehouse stock only after successful save"""
    warehouse = instance.product.warehouse

    if instance.status == SaleProduct.SaleProductStatusChoices.RETURNED:
        warehouse.quantity += instance.quantity  # Increment if returned
    else:
        warehouse.quantity -= instance.quantity  # Decrement if sold

    warehouse.save()