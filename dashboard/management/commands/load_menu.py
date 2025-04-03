from django.core.management.base import BaseCommand
from dashboard.models import MenuItem

class Command(BaseCommand):
    help = 'Loads menu items into the database'

    def handle(self, *args, **kwargs):
        menu_items = [
            # Burgers / Sandwiches
            ('Cheeseburger', 8.99),
            ('Double Cheeseburger', 11.99),
            ('Bacon Cheeseburger', 10.99),
            ('Classic Burger', 7.99),
            ('Veggie Burger', 8.49),
            ('Chicken Burger', 9.49),
            ('Spicy Chicken Sandwich', 9.99),

            # Sides
            ('Fries', 3.99),
            ('Onion Rings', 3.99),
            ('Poutine', 5.99),
            ('Mozzarella Sticks (6pc)', 5.49),

            # Beverages
            ('Coke', 1.50),
            ('Ginger Ale', 1.50),
            ('Sprite', 1.50),
            ('Water Bottle', 1.00),
            ('Iced Tea', 1.75),
            ('Root Beer', 1.50),
            ('Milkshake', 3.99),

            # Dessert
            ('Chocolate Sundae', 3.49),
        ]

        for name, price in menu_items:
            MenuItem.objects.create(item_name=name, price=price)

        self.stdout.write(self.style.SUCCESS('✅ Menu items loaded successfully!'))
