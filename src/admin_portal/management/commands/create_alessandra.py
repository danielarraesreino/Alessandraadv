from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
import os

class Command(BaseCommand):
    help = 'Create the definitive production user for Alessandra'

    def handle(self, *args, **options):
        # 1. Get password from environment or use a placeholder (to be changed)
        password = os.environ.get('ALESSANDRA_PASSWORD', 'Alessandra@2026')
        
        # 2. Create or Update Superuser
        user, created = User.objects.get_or_create(
            username='alessandra',
            defaults={
                'email': 'alessandra@donadon.adv.br',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        user.set_password(password)
        user.save()

        # 3. Assign to Manager Group
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        user.groups.add(manager_group)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'User "alessandra" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'User "alessandra" updated successfully.'))
        
        self.stdout.write(self.style.WARNING(f'IMPORTANT: Password is set to {"environment variable ALESSANDRA_PASSWORD" if os.environ.get("ALESSANDRA_PASSWORD") else "default value"}.'))
