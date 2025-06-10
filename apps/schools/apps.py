import logging
from importlib import import_module

from django.apps import AppConfig

from apps.home.config.auth import auth_config

logger = logging.getLogger(__name__)


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.schools"

    def ready(self):
        try:
            # Register roles specific to schools with staff status configuration
            auth_config.register_roles(
                [
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

            # Disable signup page
            auth_config.disable_page("signup")

            # Set username field label
            auth_config.configure_username_field(
                label="School ID", placeholder="Enter your School ID"
            )

            # Import signals to ensure signal handlers are registered
            import_module(f"{self.name}.signals")

        except Exception as e:
            logger.warning(f"Failed to configure school app settings: {e}")
