from django.core.management.base import BaseCommand
from dashboard.models import MenuItem, InventoryItem, MenuItemIngredient, Supplier

class Command(BaseCommand):
    help = 'Loads menu item ingredient relationships with correct supplier links'

    def handle(self, *args, **kwargs):
        # Supplier mapping based on ingredient name
        ingredient_supplier_map = {
            'Lettuce': 1,
            'Tomatoes': 1,
            'Onion': 1,
            'Cheese': 2,
            'Milk': 2,
            'Veggie Patty': 3,
            'Burger Sauce': 4,
            'Spicy Sauce': 4,
            'Beef Patty': 5,
            'Bacon': 5,
            'Chicken Patty': 5,
            'Coke': 6,
            'Ginger Ale': 6,
            'Sprite': 6,
            'Root Beer': 6,
            'Tea': 6,
            'Bread Bun': 8,
            'Potatoes': 9,
            'Mozzarella': 10,
            'Gravy': 10,
            'Ice Cream': 10,
        }

        data = [
            # Menu Item                  Ingredient         Quantity
            ('Cheeseburger',             'Bread Bun',       1),
            ('Cheeseburger',             'Beef Patty',      1),
            ('Cheeseburger',             'Cheese',          1),
            ('Cheeseburger',             'Lettuce',         30),
            ('Cheeseburger',             'Tomatoes',        30),
            ('Cheeseburger',             'Burger Sauce',    20),

            ('Double Cheeseburger',      'Bread Bun',       1),
            ('Double Cheeseburger',      'Beef Patty',      2),
            ('Double Cheeseburger',      'Cheese',          2),
            ('Double Cheeseburger',      'Lettuce',         30),
            ('Double Cheeseburger',      'Tomatoes',        30),
            ('Double Cheeseburger',      'Burger Sauce',    20),

            ('Bacon Cheeseburger',       'Bread Bun',       1),
            ('Bacon Cheeseburger',       'Beef Patty',      1),
            ('Bacon Cheeseburger',       'Cheese',          1),
            ('Bacon Cheeseburger',       'Lettuce',         30),
            ('Bacon Cheeseburger',       'Tomatoes',        30),
            ('Bacon Cheeseburger',       'Burger Sauce',    20),
            ('Bacon Cheeseburger',       'Bacon',           2),

            ('Classic Burger',           'Bread Bun',       1),
            ('Classic Burger',           'Beef Patty',      1),
            ('Classic Burger',           'Lettuce',         30),
            ('Classic Burger',           'Tomatoes',        30),
            ('Classic Burger',           'Burger Sauce',    20),

            ('Veggie Burger',            'Bread Bun',       1),
            ('Veggie Burger',            'Veggie Patty',    1),
            ('Veggie Burger',            'Lettuce',         30),
            ('Veggie Burger',            'Tomatoes',        30),
            ('Veggie Burger',            'Burger Sauce',    20),

            ('Chicken Burger',           'Bread Bun',       1),
            ('Chicken Burger',           'Chicken Patty',   1),
            ('Chicken Burger',           'Lettuce',         30),
            ('Chicken Burger',           'Burger Sauce',    20),

            ('Spicy Chicken Sandwich',   'Bread Bun',       1),
            ('Spicy Chicken Sandwich',   'Chicken Patty',   1),
            ('Spicy Chicken Sandwich',   'Spicy Sauce',     15),

            ('Fries',                    'Potatoes',        250),
            ('Onion Rings',              'Onion',           150),
            ('Poutine',                  'Potatoes',        250),
            ('Poutine',                  'Gravy',           100),
            ('Poutine',                  'Cheese',          1),

            ('Mozzarella Sticks (6pc)',  'Mozzarella',      6),

            ('Coke',                     'Coke',            1),
            ('Ginger Ale',               'Ginger Ale',      1),
            ('Sprite',                   'Sprite',          1),
            ('Root Beer',                'Root Beer',       1),
            ('Iced Tea',                 'Tea',             1),

            ('Milkshake',                'Milk',            250),
            ('Milkshake',                'Ice Cream',       1),

            ('Chocolate Sundae',         'Ice Cream',       2),
        ]

        for menu_name, ingredient_name, quantity in data:
            try:
                menu_item = MenuItem.objects.get(item_name=menu_name)
                ingredient = InventoryItem.objects.get(ingredient=ingredient_name)
                supplier_id = ingredient_supplier_map[ingredient_name]
                supplier = Supplier.objects.get(id=supplier_id)

                MenuItemIngredient.objects.create(
                    menu_item=menu_item,
                    ingredient=ingredient,
                    quantity_used=quantity,
                    supplier=supplier
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Failed for {menu_name} / {ingredient_name}: {e}'))

        self.stdout.write(self.style.SUCCESS('✅ Menu item ingredients with suppliers loaded successfully!'))
