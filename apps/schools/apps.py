import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.schools"
    verbose_name = "Functional Modules"

    def ready(self):
        try:
            # Only configure non-role related auth settings
            from apps.home.config.auth import auth_config

            # Configure page settings (no role management needed)
            auth_config.disable_page("signup")
            auth_config.configure_username_field(
                label="School ID", placeholder="Enter your School ID"
            )

            logger.info("School app configured successfully")

        except Exception as e:
            logger.warning(f"Failed to configure school app settings: {e}")
