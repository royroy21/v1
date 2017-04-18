from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = get_user_model().objects.create(
            username='admin',
            is_superuser=True,
            is_staff=True)
        admin.set_password('Pa$$word')
        admin.save()

        self.stdout.write(self.style.SUCCESS('Admin created'))