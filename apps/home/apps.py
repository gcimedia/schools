import logging
from importlib import import_module

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"
    verbose_name = "Base"

    def ready(self):
        # ********* Import signals to ensure they are registered
        try:
            import_module(f"{self.name}.signals")
        except ImportError as e:
            print(f"Error importing signals: {e}")

        # ********* Home App Configuration *********
        try:
            from .config.landing import landing_config
            from .config.navigation import nav_config

            # Configure landing url
            landing_config.register_landing_url("landing", f"{self.name}")

            # Add landing url to nav items
            nav_config.register("Home", "landing", fragment="hero", order=0)

        except Exception as e:
            logger.warning(f"Failed to configure home app settings: {e}")
