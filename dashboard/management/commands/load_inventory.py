from django.core.management.base import BaseCommand
from dashboard.models import InventoryItem

class Command(BaseCommand):
    help = 'Loads inventory items into the database'

    def handle(self, *args, **kwargs):
        inventory = [
            # Ingredient           Unit      Quantity  Reorder  Status
            ('Cheese',            'slices',  100,      25,     'In Stock'),
            ('Beef Patty',        'pcs',     100,      25,     'In Stock'),
            ('Bread Bun',         'pcs',     100,      25,     'In Stock'),
            ('Bacon',             'slices',  50,       10,     'In Stock'),
            ('Coke',              'cans',    10,       10,     'Low Stock'),
            ('Ginger Ale',        'cans',    50,       10,     'In Stock'),
            ('Sprite',            'cans',    50,       10,     'In Stock'),
            ('Root Beer',         'cans',    50,       10,     'In Stock'),
            ('Iced Tea',          'cans',    30,       10,     'In Stock'),
            ('Potatoes',          'grams',   3000,     1000,   'In Stock'),
            ('Tomatoes',          'grams',   2000,     500,    'In Stock'),
            ('Lettuce',           'grams',   0,        500,    'Out of Stock'),
            ('Onion',             'grams',   500,      500,    'Low Stock'),
            ('Chicken Patty',     'pcs',     50,       15,     'In Stock'),
            ('Veggie Patty',      'pcs',     25,       10,     'In Stock'),
            ('Mozzarella',        'sticks',  40,       20,     'In Stock'),
            ('Gravy',             'ml',      2000,     500,    'In Stock'),
            ('Milk',              'ml',      1000,     250,    'In Stock'),
            ('Ice Cream',         'scoops',  100,      25,     'In Stock'),
            ('Tea',               'bags',    30,       10,     'In Stock'),
            ('Burger Sauce',      'ml',      500,      100,    'In Stock'),
            ('Spicy Sauce',       'ml',      200,      50,     'In Stock'),
        ]

        for name, unit, qty, reorder, status in inventory:
            InventoryItem.objects.create(
                ingredient=name,
                unit=unit,
                quantity_in_stock=qty,
                reorder_level=reorder,
                stock_status=status
            )

        self.stdout.write(self.style.SUCCESS('✅ Inventory items loaded successfully!'))
