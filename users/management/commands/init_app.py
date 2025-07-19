from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction


class Command(BaseCommand):
    help = "Initial setup: migrate, create demo data, etc."

    ordered_commands = [
        ("populate_demo_data", "🧪 Loading initial structure..."),
        ("populate_residents", "👥 Creating demo residents..."),         #for test systems
        ("populate_task_templates", "🗂 Creating task templates..."),    #for test systems
        ("populate_demo_assignments", "📝 Assigning tasks..."),          #for test systems
        ("populate_resident_role_assignments", "🎭 Assigning roles..."), #for test systems
        ("populate_demo_reports", "📊 Populating reports..."),           #for test systems
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reinitialization even if users exist.'
        )

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting full initialization process...")

        User = get_user_model()
        if User.objects.exists() and not options['force']:
            self.stdout.write("✅ Users already exist — skipping demo initialization.")
            return

        try:
            for command, message in self.ordered_commands:
                self.stdout.write(message)
                with transaction.atomic():
                    call_command(command)
                    self.stdout.write(self.style.SUCCESS(f"✅ {command} completed successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error during '{command}': {e}"))
            raise

        self.stdout.write(self.style.SUCCESS("🎉 All demo data successfully initialized."))