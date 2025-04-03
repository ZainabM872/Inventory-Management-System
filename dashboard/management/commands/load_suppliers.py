from django.core.management.base import BaseCommand
from dashboard.models import Supplier, ContactInfo

class Command(BaseCommand):
    help = 'Loads suppliers and their contact information'

    def handle(self, *args, **kwargs):
        # Supplier company names
        suppliers = {
            1: 'Fresh Foods',
            2: 'DairyPro',
            3: 'Veggie Fresh Supply',
            4: 'Sauce Depot',
            5: 'Meat Masters',
            6: 'DrinkSource',
            7: 'PaperCo',
            8: 'Bun Brothers',
            9: 'Greenleaf Farms',
            10: 'Essentials Inc.'
        }

        supplier_objs = {}

        for id_, name in suppliers.items():
            obj = Supplier.objects.create(id=id_, company_name=name)
            supplier_objs[id_] = obj

        # Contact info (only for some suppliers)
        contact_data = [
            (1, 'fresh@example.com', '555-1234'),
            (2, 'dairy@example.com', '555-5678'),
            (4, 'sauce@example.com', '555-3344'),
            (5, 'meat@example.com', '555-5566'),
            (6, 'drink@example.com', '555-7788'),
            (7, 'paperco@example.com', '555-9900'),
            (8, 'buns@example.com', '555-2121'),
            (9, 'greenleaf@example.com', '555-3131'),
            (10, 'essentials@example.com', '555-4141'),
        ]

        for supplier_id, email, phone in contact_data:
            ContactInfo.objects.create(
                supplier=supplier_objs[supplier_id],
                email=email,
                phone=phone
            )

        self.stdout.write(self.style.SUCCESS('✅ Suppliers and contact info loaded successfully!'))
