import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.home.models import UserGroup

logger = logging.getLogger(__name__)
User = get_user_model()


class Command(BaseCommand):
    help = "Set up initial user roles and update existing users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update existing roles (will overwrite existing role settings)",
        )
        parser.add_argument(
            "--update-users",
            action="store_true",
            help="Update staff status for existing users based on their roles",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )

    def handle(self, *args, **options):
        self.verbosity = options["verbosity"]
        self.force = options["force"]
        self.update_users = options["update_users"]
        self.dry_run = options["dry_run"]

        if self.dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No changes will be made")
            )

        try:
            with transaction.atomic():
                self.setup_roles()

                if self.update_users:
                    self.update_user_staff_status()

                if self.dry_run:
                    # Rollback transaction in dry-run mode
                    raise transaction.TransactionManagementError(
                        "Dry run - rolling back"
                    )

        except transaction.TransactionManagementError:
            if not self.dry_run:
                raise
        except Exception as e:
            raise CommandError(f"Failed to setup roles: {e}")

        if not self.dry_run:
            self.stdout.write(self.style.SUCCESS("Successfully set up roles!"))

    def setup_roles(self):
        """Create or update initial roles"""
        # Define your initial roles here
        initial_roles = [
            {
                "name": "student",
                "display_name": "Student",
                "is_staff_role": False,
                "is_default_role": True,
                "description": "Standard student role with basic access",
            },
            {
                "name": "instructor",
                "display_name": "Instructor",
                "is_staff_role": True,
                "is_default_role": False,
                "description": "Teaching staff with course management access",
            },
            {
                "name": "admin",
                "display_name": "Administrator",
                "is_staff_role": True,
                "is_default_role": False,
                "description": "Full administrative access",
            },
        ]

        created_roles = []
        updated_roles = []

        for role_data in initial_roles:
            role_name = role_data["name"]

            try:
                role = UserGroup.objects.get(name=role_name)

                if self.force:
                    # Update existing role
                    role.display_name = role_data["display_name"]
                    role.is_staff_role = role_data["is_staff_role"]
                    role.is_default_role = role_data["is_default_role"]
                    role.description = role_data["description"]

                    if not self.dry_run:
                        role.save()

                    updated_roles.append(role_name)

                    if self.verbosity >= 2:
                        self.stdout.write(f"Updated role: {role_name}")
                else:
                    if self.verbosity >= 2:
                        self.stdout.write(
                            f"Role already exists: {role_name} (use --force to update)"
                        )

            except UserGroup.DoesNotExist:
                # Create new role
                if not self.dry_run:
                    role = UserGroup.objects.create(**role_data)

                created_roles.append(role_name)

                if self.verbosity >= 2:
                    self.stdout.write(f"Created role: {role_name}")

        # Summary output
        if created_roles:
            self.stdout.write(
                self.style.SUCCESS(f"Created roles: {', '.join(created_roles)}")
            )

        if updated_roles:
            self.stdout.write(
                self.style.SUCCESS(f"Updated roles: {', '.join(updated_roles)}")
            )

        if not created_roles and not updated_roles:
            self.stdout.write(self.style.WARNING("No roles were created or updated"))

    def update_user_staff_status(self):
        """Update staff status for existing users based on their roles"""
        updated_count = 0
        users_to_update = []

        for user in User.objects.exclude(is_superuser=True):
            role_obj = user.get_role_object()

            if role_obj and user.is_staff != role_obj.is_staff_role:
                users_to_update.append(
                    {
                        "user": user,
                        "old_status": user.is_staff,
                        "new_status": role_obj.is_staff_role,
                        "role": role_obj.name,
                    }
                )

        if users_to_update:
            for user_data in users_to_update:
                if not self.dry_run:
                    User.objects.filter(pk=user_data["user"].pk).update(
                        is_staff=user_data["new_status"]
                    )

                if self.verbosity >= 2:
                    self.stdout.write(
                        f"User {user_data['user'].username}: "
                        f"staff status {user_data['old_status']} -> {user_data['new_status']} "
                        f"(role: {user_data['role']})"
                    )

                updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(f"Updated staff status for {updated_count} users")
            )
        else:
            self.stdout.write(
                self.style.WARNING("No users needed staff status updates")
            )
