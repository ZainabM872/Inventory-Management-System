from django.core.management.base import BaseCommand
from dashboard.models import User, Manager, Staff, Schedule

class Command(BaseCommand):
    help = 'Loads initial user, manager, staff, and schedule data'

    def handle(self, *args, **kwargs):
        # Create users
        users = [
            {'name': 'Caio', 'password': 'caio_password'},
            {'name': 'Alisha', 'password': 'alisha_password'},
            {'name': 'Zainab', 'password': 'zainab_password'},
            {'name': 'Marco', 'password': 'marco_password'},
            {'name': 'Jasmine', 'password': 'jasmine_password'},
            {'name': 'Eli', 'password': 'eli_password'},
            {'name': 'Rosa', 'password': 'rosa_password'},
            {'name': 'Andre', 'password': 'andre_password'},
            {'name': 'Mia', 'password': 'mia_password'},
            {'name': 'Leo', 'password': 'leo_password'},
        ]

        user_objs = {}
        for user in users:
            obj = User.objects.create(name=user['name'], password=user['password'])
            user_objs[user['name']] = obj  # store for later use

        # Assign managers
        manager_names = ['Alisha', 'Jasmine', 'Andre', 'Leo']
        for name in manager_names:
            Manager.objects.create(user=user_objs[name])

        # Assign staff
        staff_names = ['Caio', 'Zainab', 'Marco', 'Eli', 'Rosa', 'Mia']
        for name in staff_names:
            Staff.objects.create(user=user_objs[name])

        # Create schedules
        schedules = [
            ('Alisha', 'Caio', '9-5', '9-5', '9-5', 'OFF', '9-5', 'OFF'),
            ('Alisha', 'Zainab', '10-6', '10-6', '10-6', '10-6', '10-6', 'OFF'),
            ('Jasmine', 'Marco', '8-4', '8-4', '8-4', '8-4', 'OFF', '4'),
            ('Jasmine', 'Eli', '9-5', '9-5', '9-5', '8-4', '9-5', 'OFF'),
            ('Andre', 'Rosa', '8-4', '9-5', 'OFF', '10-6', '10-6', 'OFF'),
            ('Andre', 'Mia', '10-6', '8-4', '8-4', '9-5', 'OFF', 'OFF'),
        ]

        for manager_name, staff_name, tue, wed, thu, fri, sat, sun in schedules:
            manager = Manager.objects.get(user=user_objs[manager_name])
            staff = Staff.objects.get(user=user_objs[staff_name])
            Schedule.objects.create(
                manager=manager,
                staff=staff,
                tuesday=tue,
                wednesday=wed,
                thursday=thu,
                friday=fri,
                saturday=sat,
                sunday=sun,
            )

        self.stdout.write(self.style.SUCCESS('✅ Team data loaded successfully!'))
