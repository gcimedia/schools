import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.schools"

    def ready(self):
        try:
            from apps.base.registry.auth import auth_registry

            auth_registry.disable_page("signup")  # Disable the signup page

        except Exception as e:
            logger.warning(f"Failed to disable signup page: {e}")
