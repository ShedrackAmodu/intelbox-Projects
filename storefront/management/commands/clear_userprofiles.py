from django.core.management.base import BaseCommand
from storefront.models import UserProfile

class Command(BaseCommand):
    help = 'Clears all UserProfile entries'

    def handle(self, *args, **kwargs):
        count, _ = UserProfile.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} UserProfile entries'))
