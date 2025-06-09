import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.schools"

    def ready(self):
        # ********* School App Configuration *********
        try:
            from apps.home.registry.auth import auth_registry

            # Disable the signup page
            auth_registry.disable_page("signup")

            # Configure username field for schools app
            auth_registry.configure_username_field(
                label="ID/Username", placeholder="Your School ID/Username"
            )

        except Exception as e:
            logger.warning(f"Failed to configure school app settings: {e}")
