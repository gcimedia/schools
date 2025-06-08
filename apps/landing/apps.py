import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class LandingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.landing"

    def ready(self):
        # Register landing page in nav_items
        try:
            from apps.base.registry.navigation import nav_registry

            nav_registry.register("Home", "landing:home", fragment="hero", order=0)

        except Exception as e:
            logger.error(f"Failed to register landing app navigation links: {e}")

        # Register landing page as home URL
        try:
            from apps.base.registry.home import home_registry

            home_registry.register_home_url("landing:home", f"{self.name}")

        except Exception as e:
            logger.error(f"Failed to register landing app home URL: {e}")
