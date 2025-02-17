import random
import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from pharmacy_app.models import (
    Staff, Sale, SalePayment, Category, UomGroup, Uom, Product, SaleProduct,
    ProductPriceHistory, BackupWarehouseProduct, WarehouseProduct
)


class Command(BaseCommand):
    help = "Populate database with test data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database population..."))

        # Create Staff Members
        admin = Staff.objects.get(username="admin")
        cashier = Staff.objects.get(username="cashier")
        warehouse = Staff.objects.get(username="warehouse")

        self.stdout.write(self.style.SUCCESS("Created staff members."))

        # Create Categories
        categories = [Category.objects.create(title=f"Category {i}") for i in range(1, 6)]
        self.stdout.write(self.style.SUCCESS("Created categories."))

        # Create UoM Groups and UoMs
        uom_group = UomGroup.objects.create(title="Default UoM Group")
        uoms = [Uom.objects.create(uomGroup=uom_group, baseQuantity=Decimal("1.00"), quantity=Decimal(str(i))) for i in
                range(1, 6)]
        self.stdout.write(self.style.SUCCESS("Created UoMs."))

        # Create Products
        products = [
            Product.objects.create(
                title=f"Product {i}",
                uom=random.choice(uoms),
                recorder=random.choice([admin, cashier, warehouse]),
                category=random.choice(categories)
            ) for i in range(1, 11)
        ]
        self.stdout.write(self.style.SUCCESS("Created products."))

        # Create Sales
        sales = [
            Sale.objects.create(
                code=str(uuid.uuid4())[:8],
                recorder=random.choice([admin, cashier]),
                totalAmount=Decimal(random.randint(100, 1000)),
                status=Sale.SaleStatusChoices.IN_PROGRESS
            ) for _ in range(5)
        ]
        self.stdout.write(self.style.SUCCESS("Created sales."))

        # Create Sale Products
        sale_products = [
            SaleProduct.objects.create(
                sale=random.choice(sales),
                product=random.choice(products),
                quantity=Decimal(random.randint(1, 5)),
                unitPrice=Decimal(random.randint(10, 100)),
                status=SaleProduct.SaleProductStatusChoices.SOLD,
            ) for _ in range(10)
        ]
        self.stdout.write(self.style.SUCCESS("Created sale products."))

        # Create Sale Payments
        sale_payments = [
            SalePayment.objects.create(
                sale=random.choice(sales),
                code=str(uuid.uuid4())[:8],
                amount=Decimal(random.randint(50, 500)),
                payment_type=random.choice([SalePayment.PaymentTypeChoices.CARD, SalePayment.PaymentTypeChoices.CASH])
            ) for _ in range(5)
        ]
        self.stdout.write(self.style.SUCCESS("Created sale payments."))

        # Create Warehouse Products
        warehouse_products = [
            WarehouseProduct.objects.create(
                product=product,
                quantity=Decimal(random.randint(10, 100)),
                unitPrice=Decimal(random.randint(10, 100)),
                recorder=random.choice([admin, warehouse])
            ) for product in products
        ]
        self.stdout.write(self.style.SUCCESS("Created warehouse products."))

        # Create Backup Warehouse Products
        backup_products = [
            BackupWarehouseProduct.objects.create(
                product=product,
                quantity=Decimal(random.randint(5, 50)),
                unitPrice=Decimal(random.randint(5, 50))
            ) for product in products
        ]
        self.stdout.write(self.style.SUCCESS("Created backup warehouse products."))

        # Create Product Price History
        price_history = [
            ProductPriceHistory.objects.create(
                product=product,
                oldPrice=Decimal(random.randint(10, 90)),
                newPrice=Decimal(random.randint(10, 100)),
                recorder=random.choice([admin, cashier])
            ) for product in products
        ]
        self.stdout.write(self.style.SUCCESS("Created product price history."))

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
