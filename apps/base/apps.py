import logging
from importlib import import_module

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class BaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.base"
    verbose_name = "(Organization) Base"

    def ready(self):
        # ********* Import signals to ensure they are registered
        try:
            import_module(f"{self.name}.signals")
        except ImportError as e:
            print(f"Error importing signals: {e}")

        # ********* Register landing page in nav_items *********
        try:
            from .registry.navigation import nav_registry

            nav_registry.register("Home", "landing", fragment="hero", order=0)

        except Exception as e:
            logger.error(f"Failed to register landing app navigation links: {e}")

        # ********* Register landing page as home URL *********
        try:
            from .registry.landing import landing_registry

            landing_registry.register_landing_url("landing", f"{self.name}")

        except Exception as e:
            logger.error(f"Failed to register landing app home URL: {e}")
