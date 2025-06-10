# Create this file: apps/schools/management/commands/sync_staff_status.py

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.home.config.auth import auth_config

User = get_user_model()


class Command(BaseCommand):
    help = "Sync staff status for all users based on their role groups"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        updated_count = 0

        self.stdout.write("Syncing staff status for all users...")

        for user in User.objects.all():
            if user.is_superuser:
                continue  # Skip superusers

            current_role = user.get_role()
            if current_role and current_role != "No role assigned":
                should_be_staff = auth_config.get_role_staff_status(current_role)

                if user.is_staff != should_be_staff:
                    self.stdout.write(
                        f"User {user.username} ({current_role}): "
                        f"is_staff {user.is_staff} -> {should_be_staff}"
                    )

                    if not dry_run:
                        user.is_staff = should_be_staff
                        user.save(update_fields=["is_staff"])

                    updated_count += 1

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"Would update {updated_count} users (dry run)")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully updated {updated_count} users")
            )
