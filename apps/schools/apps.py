# apps/schools/apps.py

import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from apps.home.config.auth import auth_config

logger = logging.getLogger(__name__)


def setup_school_roles(sender, **kwargs):
    """Setup roles and groups after migrations"""
    try:
        # Create the groups if they don't exist
        created_groups = auth_config.create_groups_if_needed()
        if created_groups:
            logger.info(
                f"School roles and groups created successfully: {created_groups}"
            )
        else:
            logger.info("All school roles and groups already exist")

        # Update staff status for all existing users based on their roles
        updated_count = auth_config.bulk_update_staff_status()
        if updated_count > 0:
            logger.info(f"Updated staff status for {updated_count} users")

    except Exception as e:
        logger.warning(f"Failed to create school groups or update staff status: {e}")


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.schools"

    def ready(self):
        try:
            # Register roles specific to schools with staff status configuration
            auth_config.register_roles(
                [
                    # Method 1: Using dictionaries for full configuration
                    {"name": "student", "display_name": "Student", "is_staff": False},
                    {
                        "name": "instructor",
                        "display_name": "Instructor",
                        "is_staff": False,
                    },
                    {
                        "name": "admin",
                        "display_name": "Administrator",
                        "is_staff": True,
                    },
                ],
                default_role="student",
            )

            # Set role permissions
            auth_config.set_role_permissions(
                "student", ["view_module", "view_enrollment"]
            )
            auth_config.set_role_permissions(
                "instructor",
                [
                    "view_module",
                    "view_enrollment",
                    "add_enrollment",
                ],
            )
            auth_config.set_role_permissions(
                "admin",
                [
                    "view_school",
                    "add_school",
                    "change_school",
                    "delete_school",
                    "add_module",
                    "view_module",
                    "change_module",
                    "delete_module",
                    "add_enrollment",
                    "change_enrollment",
                    "delete_enrollment",
                ],
            )
            
            # Disable the signup page
            auth_config.disable_page("signup")

            # Configure username field for schools app
            auth_config.configure_username_field(
                label="School ID", placeholder="Enter your School ID"
            )

            # Connect post_migrate signal to create groups and update staff status
            post_migrate.connect(setup_school_roles, sender=self)

            logger.info("Schools app configuration completed successfully")
            logger.info(f"Staff roles configured: {auth_config.get_staff_roles()}")

        except Exception as e:
            logger.warning(f"Failed to configure school app settings: {e}")

    def __str__(self):
        return "Schools Application"
