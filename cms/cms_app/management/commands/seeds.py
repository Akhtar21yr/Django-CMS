from django_seed import Seed
from django.core.management.base import BaseCommand
from cms_app.models import CustomUser
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Seed data for admin user'

    def handle(self, *args, **options):
        while True:
            try:
                count = int(input("Enter the number of data you want to add: "))
                if count > 0:
                    break
                else:
                    self.stdout.write(self.style.ERROR('Please enter a positive non-zero number.'))
            except ValueError:
                self.stdout.write(self.style.ERROR('Please enter a valid integer.'))

        seeder = Seed.seeder()
        seeder.add_entity(
            CustomUser,
            count,
            {
                'email': lambda x : seeder.faker.email(),
                'full_name': lambda x :seeder.faker.name(),
                'password':lambda x : make_password(seeder.faker.password()),
                'phone': lambda x : seeder.faker.phone_number(),
                'address' : lambda x : seeder.faker.address(),
                "city" : lambda x : seeder.faker.city(),
                'state' : lambda x : seeder.faker.state(),
                "country" : lambda x : seeder.faker.country(),
                "pincode" : lambda x : seeder.faker.zipcode(),
                'is_admin': True,
                # Add other fields as needed
            },
        )
        inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'Admin user seed data created successfully. PKs: {inserted_pks}'))