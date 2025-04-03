from django.core.management.base import BaseCommand
from dashboard.models import (
    SupplyOrder, SupplyOrderDetail, Supplier, Manager,
    InventoryItem, MenuOrder, MenuItem, Staff
)
from datetime import datetime

class Command(BaseCommand):
    help = 'Loads supply and menu orders into the database'

    def handle(self, *args, **kwargs):
       
        supply_orders = [
            (2, 2, '2025-03-15 22:58:24', '2025-03-20', 120.50, 'Completed'),   # DairyPro – Cheese
            (5, 5, '2025-03-15 16:15:57', '2025-03-26', 152.18, 'Cancelled'),   # Meat Masters – Beef Patty
            (8, 6, '2025-03-20 12:19:56', '2025-03-26', 88.72, 'Pending'),      # DrinkSource – Coke
            (5, 6, '2025-03-22 00:26:32', '2025-03-25', 198.55, 'Pending'),     # DrinkSource – Ginger Ale
            (8, 6, '2025-03-09 09:50:49', '2025-03-27', 109.22, 'Pending'),     # DrinkSource – Sprite
            (10, 9, '2025-03-10 09:50:49', '2025-03-28', 120.22, 'Pending'),    # Greenleaf Farms – Potatoes
            (2, 1, '2025-03-11 09:50:49', '2025-03-29', 130.22, 'Pending'),     # Fresh Foods – Lettuce
            (5, 1, '2025-03-12 09:50:49', '2025-03-20', 150.22, 'Pending'),     # Fresh Foods – Onion
        ]

        supply_order_objs = []
        for manager_id, supplier_id, order_dt, delivery_dt, cost, status in supply_orders:
            manager = Manager.objects.get(user__id=manager_id)
            supplier = Supplier.objects.get(id=supplier_id)
            obj = SupplyOrder.objects.create(
                manager=manager,
                supplier=supplier,
                order_date=datetime.strptime(order_dt, '%Y-%m-%d %H:%M:%S'),
                delivery_date=delivery_dt,
                total_cost=cost,
                status=status
            )
            supply_order_objs.append(obj)

        
        supply_order_details = [
            (1, 2, 'Cheese', 100),           # DairyPro
            (2, 5, 'Beef Patty', 50),        # Meat Masters
            (3, 6, 'Coke', 50),              # DrinkSource
            (4, 6, 'Ginger Ale', 50),        # DrinkSource
            (5, 6, 'Sprite', 50),            # DrinkSource
            (6, 9, 'Potatoes', 30),          # Greenleaf Farms
            (7, 1, 'Lettuce', 25),           # Fresh Foods
            (8, 1, 'Onion', 30),             # Fresh Foods
        ]

        for supply_order_id, supplier_id, ingredient_name, qty in supply_order_details:
            ingredient = InventoryItem.objects.get(ingredient=ingredient_name)
            supply_order = SupplyOrder.objects.get(id=supply_order_id)
            supplier = Supplier.objects.get(id=supplier_id)
            SupplyOrderDetail.objects.create(
                supply_order=supply_order,
                supplier=supplier,
                ingredient=ingredient,
                quantity_ordered=qty
            )

        # 
        menu_orders = [
            ('Cheeseburger', 1, 1),
            ('Double Cheeseburger', 2, 1),
            ('Bacon Cheeseburger', 1, 3),
            ('Coke', 2, 3),
            ('Ginger Ale', 1, 4),
            ('Sprite', 1, 4),
            ('Fries', 1, 1),
            ('Onion Rings', 1, 4),
        ]

        for item_name, qty, staff_id in menu_orders:
            item = MenuItem.objects.get(item_name=item_name)
            staff = Staff.objects.get(user__id=staff_id)
            MenuOrder.objects.create(
                item=item,
                item_quantity=qty,
                staff=staff
            )

        self.stdout.write(self.style.SUCCESS('✅ Supply and menu orders loaded successfully!'))
