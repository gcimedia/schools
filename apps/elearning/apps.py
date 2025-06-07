import logging
from importlib import import_module

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class ElearningConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.elearning"

    def ready(self):
        try:
            import_module(f"{self.name}.registry")
        except ImportError as e:
            logger.warning(f"Could not import registry module for {self.name}: {e}")
