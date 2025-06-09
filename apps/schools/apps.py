import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.schools"

    def ready(self):
        # ********* School App Configuration *********
        try:
            from apps.home.config.auth import auth_config

            # Disable the signup page
            auth_config.disable_page("signup")

            # Configure username field for schools app
            auth_config.configure_username_field(
                label="ID/Username", placeholder="Your School ID/Username"
            )

        except Exception as e:
            logger.warning(f"Failed to configure school app settings: {e}")
