import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from pharmacy_app.models import Staff, Sale, Category, Product, SaleProduct, ProductPriceHistory, ProductBatch


class Command(BaseCommand):
    help = "Populate the database with test data"

    def handle(self, *args, **kwargs):
        # Create Staff
        admin = Staff.objects.create_user(username="admin", first_name="Admin", role=Staff.StaffRoleChoices.ADMIN,
                                          password="0000")
        cashier = Staff.objects.create_user(username="cashier", first_name="Cashier", role=Staff.StaffRoleChoices.CASHIER,
                                            password="0000")
        warehouse = Staff.objects.create_user(username="warehouse", first_name="Warehouse",
                                              role=Staff.StaffRoleChoices.WAREHOUSE, password="000")

        # Create Categories
        categories = [Category.objects.create(title=title) for title in ["Medicine", "Clinical", "Inhalant"]]

        # Create Products
        products = []
        for category in categories:
            for i in range(5):
                product = Product.objects.create(
                    title=f"{category.title} Product {i + 1}",
                    recorder=warehouse,
                    category=category
                )
                products.append(product)

        # Create Product Batches
        for product in products:
            batch = ProductBatch.objects.create(
                product=product,
                recorder=warehouse,
                quantity=Decimal(random.randint(10, 100)),
                unitPrice=Decimal(random.uniform(5, 50)),
                retailPrice=Decimal(random.uniform(51, 100)),
                source=ProductBatch.ProductBatchSourceChoices.PURCHASED,
            )

            # Create Price History
            ProductPriceHistory.objects.create(
                product=product,
                oldPrice=batch.unitPrice,
                newPrice=batch.retailPrice,
                recorder=warehouse
            )

        # Create Sales
        for _ in range(3):
            sale = Sale.objects.create(
                code=f"SALE-{random.randint(1000, 9999)}",
                recorder=cashier,
                totalAmount=Decimal(0),
                status=Sale.SaleStatusChoices.IN_PROGRESS,
                payment_type=random.choice([Sale.PaymentTypeChoices.CARD, Sale.PaymentTypeChoices.CASH])
            )

            total_amount = Decimal(0)
            for _ in range(2):
                product = random.choice(products)
                quantity = Decimal(random.randint(1, 5))
                retail_price = product.batches.first().retailPrice
                sale_product = SaleProduct.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    retailPrice=retail_price,
                    status=SaleProduct.SaleProductStatusChoices.SOLD
                )
                total_amount += quantity * retail_price

            sale.totalAmount = total_amount
            sale.status = Sale.SaleStatusChoices.CLOSED
            sale.save()

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
