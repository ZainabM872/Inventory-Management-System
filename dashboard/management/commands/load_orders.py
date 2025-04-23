from django.core.management.base import BaseCommand
from dashboard.models import (
    SupplyOrder, SupplyOrderDetail, Supplier, Manager,
    InventoryItem, MenuOrder, MenuItem, Staff, MenuOrderItem, User
)
from datetime import datetime
from collections import defaultdict

user_ids = {user.name: user.id for user in User.objects.all()}

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
            # Staff 1 (User 1)
            ('Cheeseburger', 1, user_ids['Caio']),
            ('Double Cheeseburger', 2, user_ids['Caio']),
            ('Fries', 1, user_ids['Caio']),
            ('Coke', 2, user_ids['Caio']),

            # Staff 2 (User 2)
            ('Onion Rings', 2, user_ids['Zainab']),
            ('Sprite', 1, user_ids['Zainab']),
            ('Ginger Ale', 1, user_ids['Zainab']),

            # Staff 3 (User 3)
            ('Bacon Cheeseburger', 2, user_ids['Marco']),
            ('Fries', 1, user_ids['Marco']),
            ('Coke', 1, user_ids['Marco']),

            # Staff 4 (User 4)
            ('Cheeseburger', 3, user_ids['Eli']),
            ('Fries', 2, user_ids['Eli']),
            ('Ginger Ale', 1, user_ids['Eli']),
            ('Sprite', 2, user_ids['Eli']),

            # Staff 5 (User 5)
            ('Double Cheeseburger', 1, user_ids['Rosa']),
            ('Coke', 1, user_ids['Rosa']),
            ('Onion Rings', 1, user_ids['Rosa']),
        ]

        grouped_orders = defaultdict(list)

        for item_name, qty, staff_id in menu_orders:
            grouped_orders[staff_id].append((item_name, qty))

        for staff_id, items in grouped_orders.items():
            staff = Staff.objects.get(user__id=staff_id)
            order = MenuOrder.objects.create(staff=staff)

            for item_name, qty in items:
                item = MenuItem.objects.get(item_name=item_name)
                MenuOrderItem.objects.create(order=order, item=item, quantity=qty)

        self.stdout.write(self.style.SUCCESS('✅ Supply and menu orders loaded successfully!'))
