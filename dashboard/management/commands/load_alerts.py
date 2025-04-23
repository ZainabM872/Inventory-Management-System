# dashboard/management/commands/load_alerts.py

from django.core.management.base import BaseCommand
from dashboard.models import InventoryItem, Alert

class Command(BaseCommand):
    help = 'Loads stock alerts for low/out of stock inventory items'

    def handle(self, *args, **kwargs):
        alert_data = [
            # (ingredient_name, alert_type)
            ('Lettuce', 'Out of Stock'),
            ('Onion', 'Low Stock'),
        ]

        for ingredient_name, alert_type in alert_data:
            try:
                ingredient = InventoryItem.objects.get(ingredient=ingredient_name)

                # Check if alert already exists to avoid duplicates
                if not Alert.objects.filter(ingredient=ingredient, alert_type=alert_type, resolved=False).exists():
                    Alert.objects.create(
                        ingredient=ingredient,
                        alert_type=alert_type,
                        resolved=False
                    )
                    self.stdout.write(self.style.SUCCESS(f'✅ Alert created for {ingredient_name} ({alert_type})'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️ Alert already exists for {ingredient_name} ({alert_type})'))

            except InventoryItem.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Ingredient not found: {ingredient_name}'))

        self.stdout.write(self.style.SUCCESS('✅ Alert(s) loaded successfully!'))
