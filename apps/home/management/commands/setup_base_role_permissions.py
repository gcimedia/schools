import json
import logging

from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.home.models import UserRole

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Set up permissions for user roles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--role",
            type=str,
            help="Specific role to set up permissions for",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without making changes",
        )
        parser.add_argument(
            "--permissions-data",
            type=str,
            help="JSON string of permissions data to set up. Overrides hardcoded permissions.",
            required=False,
        )

    def handle(self, *args, **options):
        self.verbosity = options["verbosity"]
        self.dry_run = options["dry_run"]
        role_name = options.get("role")
        self.permissions_data_json = options.get("permissions_data")

        if self.dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No changes will be made")
            )

        try:
            with transaction.atomic():
                if role_name:
                    self.setup_role_permissions(role_name)
                else:
                    self.setup_all_role_permissions()

                if self.dry_run:
                    raise transaction.TransactionManagementError(
                        "Dry run - rolling back"
                    )

        except transaction.TransactionManagementError:
            if not self.dry_run:
                raise
        except Exception as e:
            raise CommandError(f"Failed to setup role permissions: {e}")

        if not self.dry_run:
            self.stdout.write(
                self.style.SUCCESS("Successfully set up role permissions!")
            )

    def get_role_permissions_data(self):
        """Get role permissions data from JSON argument or use hardcoded defaults"""
        if self.permissions_data_json:
            try:
                role_permissions = json.loads(self.permissions_data_json)
                self.stdout.write(
                    self.style.SUCCESS("Using permissions data from argument.")
                )
                return role_permissions
            except json.JSONDecodeError:
                raise CommandError(
                    "Invalid JSON provided for --permissions-data argument."
                )
        else:
            # Hardcoded default permissions
            role_permissions = {
                # pass hardcoded permissions
            }
            self.stdout.write(self.style.WARNING("Using hardcoded permission sets."))
            return role_permissions

    def setup_all_role_permissions(self):
        """Set up permissions for all roles"""
        role_permissions = self.get_role_permissions_data()

        for role_name, permissions in role_permissions.items():
            self.setup_role_permissions(role_name, permissions)

    def setup_role_permissions(self, role_name, permissions=None):
        """Set up permissions for a specific role"""
        try:
            role = UserRole.objects.get(name=role_name)
        except UserRole.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Role "{role_name}" does not exist'))
            return

        if permissions is None:
            # If no permissions provided, get from data source
            role_permissions = self.get_role_permissions_data()
            permissions = role_permissions.get(role_name, [])

        self.stdout.write(f"Setting up permissions for role: {role_name}")

        if not permissions:
            self.stdout.write(
                self.style.WARNING(f"No permissions defined for role: {role_name}")
            )
            return

        valid_permissions = []
        for perm in permissions:
            try:
                if "." in perm:
                    app_label, codename = perm.split(".", 1)  # Split only on first dot
                    permission_obj = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                    valid_permissions.append(permission_obj)
                    if self.verbosity >= 2:
                        self.stdout.write(f"  ✓ {perm}")
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  ✗ Invalid permission format: {perm}")
                    )
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"  ✗ Permission not found: {perm}")
                )

        if not self.dry_run and valid_permissions:
            # Clear existing permissions and set new ones
            role.permissions.clear()
            role.permissions.add(*valid_permissions)

        self.stdout.write(
            self.style.SUCCESS(
                f'Set {len(valid_permissions)} permissions for role "{role_name}"'
            )
        )

    def get_default_permissions_for_role(self, role_name):
        """Get default permissions based on role name (kept for backward compatibility)"""
        role_permissions = self.get_role_permissions_data()
        return role_permissions.get(role_name, [])
