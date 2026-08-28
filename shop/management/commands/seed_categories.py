from django.core.management.base import BaseCommand
from shop.models import Category

CATEGORIES = [
    "Safety Apron",
    "Kitchen Apron",
    "Leather Gloves",
    "Safety Gloves",
    "Leather Belt",
    "Leather Wallet",
]

class Command(BaseCommand):
    help = "Seed the default product categories"

    def handle(self, *args, **kwargs):
        for name in CATEGORIES:
            obj, created = Category.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")
