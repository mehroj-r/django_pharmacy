from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import SaleProduct, ProductPriceHistory, ProductBatch, Sale
from django.db.models import Sum
from pharmacy_app.utils.thread_local import get_current_user

@receiver(pre_save, sender=ProductBatch)
def handle_price_change(sender, instance, **kwargs):
    """Detect retail price change before saving"""

    if instance.pk:  # Only check updating, not creating

        if sender.retailPrice != instance.retailPrice:
            recorder = get_current_user()

            ProductPriceHistory.objects.create(
                product=instance.product,
                oldPrice=sender.retailPrice,
                newPrice=instance.retailPrice,
                recorder=recorder
            )

@receiver(post_save, sender=SaleProduct)
def update_batch_stock(sender, instance, created, **kwargs):
    """Update batch stock only after successful save"""

    if not created: # If being updated, check if the status has changed

        if sender.status == instance.status:
            return


    if instance.status == SaleProduct.SaleProductStatusChoices.RETURNED: # If returned save as a new batch

        recorder = get_current_user()

        ProductBatch.objects.create(

            product=instance.product,
            recorder=recorder,

            quantity=instance.quantity,
            unitPrice=instance.retailPrice,
            retailPrice=instance.retailPrice,
            source=ProductBatch.ProductBatchSourceChoices.RETURNED
        )

    elif instance.status == SaleProduct.SaleProductStatusChoices.SOLD: # If sold reduce the quantity from batch(es)

        batches = instance.product.batches.filter(retailPrice=instance.retailPrice, quantity__gt=0).order_by('-arrival_date') # FIFO
        remaining_qty = instance.quantity
        updated_batches = []

        for batch in batches: # Look through to reduce/empty batches
            if remaining_qty == 0:
                break

            if batch.quantity >= remaining_qty:
                batch.quantity -= remaining_qty
                remaining_qty = 0
            else:
                remaining_qty -= batch.quantity
                batch.quantity = 0

            updated_batches.append(batch)

        if updated_batches:
            ProductBatch.objects.bulk_update(updated_batches, ['quantity'])
    else:
        pass # Don't process anything while pending

@receiver(post_save, sender=Sale)
def handle_sale_finish(sender, instance, **kwargs):
    """Marks every item as sold after"""

    if sender.status == Sale.SaleStatusChoices.IN_PROGRESS and instance.status == Sale.SaleStatusChoices.CLOSED:

        sale_products = instance.sale_products

        for product in sale_products:
            product.status = SaleProduct.SaleProductStatusChoices.SOLD
            product.save()

