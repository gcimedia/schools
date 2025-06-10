from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.home.models import UserGroup


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

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        role_name = options.get("role")

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

    def setup_all_role_permissions(self):
        """Set up permissions for all roles"""
        # Define permission sets for each role
        role_permissions = {
            "student": [
                # Basic permissions students might need
                "home.view_user",  # Can view their own profile
            ],
            "instructor": [
                # Instructor permissions
                "home.view_user",
                "home.change_user",  # Can edit student profiles
                # Add your app-specific permissions here
                # 'courses.add_course',
                # 'courses.change_course',
                # 'assignments.add_assignment',
            ],
            "admin": [
                # Admin gets broader permissions
                "home.add_user",
                "home.change_user",
                "home.delete_user",
                "home.view_user",
                "home.add_usergroup",
                "home.change_usergroup",
                "home.delete_usergroup",
                "home.view_usergroup",
                # Add all other permissions admins should have
            ],
        }

        for role_name, permissions in role_permissions.items():
            self.setup_role_permissions(role_name, permissions)

    def setup_role_permissions(self, role_name, permissions=None):
        """Set up permissions for a specific role"""
        try:
            role = UserGroup.objects.get(name=role_name)
        except UserGroup.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Role "{role_name}" does not exist'))
            return

        if permissions is None:
            # If no permissions provided, use default set
            permissions = self.get_default_permissions_for_role(role_name)

        self.stdout.write(f"Setting up permissions for role: {role_name}")

        valid_permissions = []
        for perm in permissions:
            try:
                if "." in perm:
                    app_label, codename = perm.split(".")
                    permission_obj = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                    valid_permissions.append(permission_obj)
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
        """Get default permissions based on role name"""
        defaults = {
            "student": ["home.view_user"],
            "instructor": ["home.view_user", "home.change_user"],
            "admin": [
                "home.add_user",
                "home.change_user",
                "home.delete_user",
                "home.view_user",
                "home.add_usergroup",
                "home.change_usergroup",
                "home.delete_usergroup",
                "home.view_usergroup",
            ],
        }
        return defaults.get(role_name, [])
