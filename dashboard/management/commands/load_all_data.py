# dashboard/management/commands/load_all_data.py

from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Loads all initial data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Starting full data load...\n')

        call_command('load_users_roles')
        call_command('load_suppliers')
        call_command('load_inventory')
        call_command('load_menu')
        call_command('load_orders')
        call_command('load_menu_ingredients')
        call_command('load_alerts')

        self.stdout.write(self.style.SUCCESS('\n✅ All data loaded successfully!'))
