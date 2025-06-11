import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

logger = logging.getLogger(__name__)


class LandingURLConfig:
    """
    Registry for managing landing URL across Django apps.
    Allows apps to register themselves as the landing URL provider.
    """

    def __init__(self):
        self._landing_url_name = None
        self._landing_app = None
        self._registered = False

    def register_landing_url(self, url_name, app_name):
        """
        Register a URL name as the landing URL.

        Args:
            url_name (str): The URL name to use as landing
            app_name (str): The app name registering the landing URL
        """
        if self._registered:
            logger.warning(
                f"Landing URL already registered by '{self._landing_app}' as '{self._landing_url_name}'. "
                f"Ignoring registration from '{app_name}' for '{url_name}'."
            )
            return False

        self._landing_url_name = url_name
        self._landing_app = app_name
        self._registered = True
        logger.info(f"Landing URL registered: '{url_name}' by app '{app_name}'")
        return True

    def get_landing_url(self):
        """
        Get the registered landing URL.

        Returns:
            str: The landing URL path

        Raises:
            ImproperlyConfigured: If no landing URL is registered
        """
        if not self._registered:
            raise ImproperlyConfigured(
                "No landing URL registered. Make sure one of your apps calls "
                "landing_config.register_landing_url() in its ready() method."
            )

        try:
            return reverse(self._landing_url_name)
        except Exception as e:
            raise ImproperlyConfigured(
                f"Could not reverse landing URL '{self._landing_url_name}' "
                f"registered by app '{self._landing_app}': {e}"
            )

    def get_landing_url_name(self):
        """Get the registered landing URL name."""
        return self._landing_url_name

    def get_landing_app(self):
        """Get the app that registered the landing URL."""
        return self._landing_app

    def is_registered(self):
        """Check if a landing URL is registered."""
        return self._registered

    def clear(self):
        """Clear the registered landing URL (useful for testing)."""
        self._landing_url_name = None
        self._landing_app = None
        self._registered = False


# Global config instance
landing_url_config = LandingURLConfig()


# Convenience functions
def register_landing_url(url_name, app_name):
    """Convenience function to register landing URL."""
    return landing_url_config.register_landing_url(url_name, app_name)


def get_landing_url():
    """Convenience function to get landing URL."""
    return landing_url_config.get_landing_url()


def get_landing_url_name():
    """Convenience function to get landing URL name."""
    return landing_url_config.get_landing_url_name()


if __name__ == "__main__":
    # ****************** Example Usage ******************

    print("=== Django Landing URL Registry Example ===\n")

    # Example 1: Basic registration and retrieval
    print("1. Basic Registration Example:")
    print("-" * 30)

    # Register a landing URL
    success = register_landing_url("dashboard:index", "dashboard")
    print(f"Registration successful: {success}")
    print(f"Landing URL name: {get_landing_url_name()}")
    print(f"Registered by app: {landing_url_config.get_landing_app()}")
    print(f"Is registered: {landing_url_config.is_registered()}")
    print()

    # Example 2: Attempt duplicate registration
    print("2. Duplicate Registration Example:")
    print("-" * 35)

    # Try to register another landing URL (should fail)
    success2 = register_landing_url("blog:landing", "blog")
    print(f"Second registration successful: {success2}")
    print(f"Landing URL name remains: {get_landing_url_name()}")
    print(f"Still registered by: {landing_url_config.get_landing_app()}")
    print()

    # Example 3: Clear and re-register
    print("3. Clear and Re-register Example:")
    print("-" * 34)

    # Clear the registry
    landing_url_config.clear()
    print(f"After clearing - Is registered: {landing_url_config.is_registered()}")

    # Register a new landing URL
    success3 = register_landing_url("blog:landing", "blog")
    print(f"New registration successful: {success3}")
    print(f"New landing URL name: {get_landing_url_name()}")
    print(f"New registered app: {landing_url_config.get_landing_app()}")
    print()

    # Example 4: Error handling
    print("4. Error Handling Example:")
    print("-" * 26)

    # Clear registry to demonstrate error
    landing_url_config.clear()
    print("Registry cleared. Attempting to get landing URL without registration...")

    try:
        url = get_landing_url()
        print(f"Landing URL: {url}")
    except ImproperlyConfigured as e:
        print(f"Expected error: {e}")
    print()

    # Example 5: How to use in Django apps
    print("5. How to Use in Django Apps:")
    print("-" * 30)
    print("""
    # In your app's apps.py file:
    
    from django.apps import AppConfig
    from core.config.urls import register_landing_url
    
    class DashboardConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'dashboard'
        
        def ready(self):
            # Register this app's landing URL
            register_landing_url('dashboard:index', 'dashboard')
    
    # In your templates:
    
    {% load url %}
    <a href="{% url landing_url_name %}">Home</a>
    
    # Or in your views:
    
    from core.config.landing import get_landing_url
    from django.shortcuts import redirect
    
    def some_view(request):
        # Redirect to landing
        return redirect(get_landing_url())
    
    # In your URL patterns:
    
    from core.config.landing import get_landing_url_name
    
    urlpatterns = [
        path('', RedirectView.as_view(url=get_landing_url()), name='root'),
        # other patterns...
    ]
    """)

    print("=== Example Complete ===")
