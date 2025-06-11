import json
import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Sets up initial school-specific user roles by calling 'setup_roles' command."
    )

    def handle(self, *args, **options):
        self.verbosity = options["verbosity"]

        # Define the list of roles specific to school setup
        initial_school_roles = [
            {
                "name": "student",
                "display_name": "Student",
                "is_staff_role": False,
                "is_default_role": True,
                "description": "Standard student role with basic access for schools",
            },
            {
                "name": "instructor",
                "display_name": "Instructor",
                "is_staff_role": True,
                "is_default_role": False,
                "description": "Teaching staff with course management access for schools",
            },
            {
                "name": "admin",
                "display_name": "Administrator",
                "is_staff_role": True,
                "is_default_role": False,
                "description": "Full administrative access for schools",
            },
            # You can add more roles specific to schools here if needed
        ]

        try:
            # Convert the list to a JSON string
            roles_json_string = json.dumps(initial_school_roles)

            # Call the 'setup_base_roles' management command, passing the JSON string
            # Pass through the verbosity from this command to setup_roles
            self.stdout.write(
                f"Calling 'setup_base_roles' with {len(initial_school_roles)} initial school roles..."
            )
            call_command(
                "setup_base_roles",
                verbosity=self.verbosity,
                roles_data=roles_json_string,
            )

            self.stdout.write(
                self.style.SUCCESS("School roles setup command completed successfully.")
            )
            logger.info("School roles setup command completed via management command")

        except Exception as e:
            logger.error(f"Failed to setup school roles: {e}")
            raise CommandError(f"Failed to setup school roles: {e}")
