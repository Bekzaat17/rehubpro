from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from .populate_demo_data import Command as PopulateCommand

class Command(BaseCommand):
    help = "Initial setup: migrate, create demo data, etc."

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Running initial setup...")

        User = get_user_model()

        if not User.objects.exists():
            self.stdout.write("🧪 No users found. Running demo setup...")
            try:
                with transaction.atomic():
                    PopulateCommand().handle()
                    self.stdout.write(self.style.SUCCESS("✅ Demo data loaded."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ Error during demo load: {e}"))
        else:
            self.stdout.write("✅ Users already exist — skipping demo init.")

        self.stdout.write(self.style.SUCCESS("🎉 Initial setup complete."))