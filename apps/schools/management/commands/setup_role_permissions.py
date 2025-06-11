import json
import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sets up school-specific role permissions by calling 'setup_base_role_permissions' command."

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
        self.verbosity = options["verbosity"]
        self.dry_run = options["dry_run"]
        role_name = options.get("role")

        # Define school-specific permission sets for each role
        school_role_permissions = {
            "student": [
                # Basic permissions students might need
                "core.view_user",  # Can view their own profile
                # Add school-specific student permissions here
                # "courses.view_course",
                # "assignments.view_assignment",
            ],
            "instructor": [
                # Instructor permissions
                "core.view_user",
                "core.change_user",  # Can edit student profiles
                # Add school-specific instructor permissions here
                # "courses.add_course",
                # "courses.change_course",
                # "courses.view_course",
                # "assignments.add_assignment",
                # "assignments.change_assignment",
                # "assignments.view_assignment",
                # "grades.add_grade",
                # "grades.change_grade",
            ],
            "admin": [
                # Admin gets broader permissions
                "core.add_user",
                "core.change_user",
                "core.delete_user",
                "core.view_user",
                "core.add_userrole",
                "core.change_userrole",
                "core.delete_userrole",
                "core.view_userrole",
                # Add school-specific admin permissions here
                # "courses.add_course",
                # "courses.change_course",
                # "courses.delete_course",
                # "courses.view_course",
                # "assignments.add_assignment",
                # "assignments.change_assignment",
                # "assignments.delete_assignment",
                # "assignments.view_assignment",
                # "grades.add_grade",
                # "grades.change_grade",
                # "grades.delete_grade",
                # "grades.view_grade",
            ],
        }

        try:
            # Convert the permissions dictionary to a JSON string
            permissions_json_string = json.dumps(school_role_permissions)

            # Prepare arguments for the base command
            base_command_args = {
                "verbosity": self.verbosity,
                "permissions_data": permissions_json_string,
            }

            # Add optional arguments if provided
            if role_name:
                base_command_args["role"] = role_name
            if self.dry_run:
                base_command_args["dry_run"] = True

            # Call the 'setup_base_role_permissions' management command
            self.stdout.write(
                "Calling 'setup_base_role_permissions' with school-specific permissions..."
            )
            call_command("setup_base_role_permissions", **base_command_args)

            self.stdout.write(
                self.style.SUCCESS(
                    "School permissions setup command completed successfully."
                )
            )
            logger.info(
                "School permissions setup command completed via management command"
            )

        except Exception as e:
            logger.error(f"Failed to setup school permissions: {e}")
            raise CommandError(f"Failed to setup school permissions: {e}")
