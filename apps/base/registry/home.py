# base/home.py
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)


class HomeURLRegistry:
    """
    Registry for managing home URL across Django apps.
    Allows apps to register themselves as the home URL provider.
    """

    def __init__(self):
        self._home_url_name = None
        self._home_app = None
        self._registered = False

    def register_home_url(self, url_name, app_name):
        """
        Register a URL name as the home URL.

        Args:
            url_name (str): The URL name to use as home
            app_name (str): The app name registering the home URL
        """
        if self._registered:
            logger.warning(
                f"Home URL already registered by '{self._home_app}' as '{self._home_url_name}'. "
                f"Ignoring registration from '{app_name}' for '{url_name}'."
            )
            return False

        self._home_url_name = url_name
        self._home_app = app_name
        self._registered = True
        logger.info(f"Home URL registered: '{url_name}' by app '{app_name}'")
        return True

    def get_home_url(self):
        """
        Get the registered home URL.

        Returns:
            str: The home URL path

        Raises:
            ImproperlyConfigured: If no home URL is registered
        """
        if not self._registered:
            raise ImproperlyConfigured(
                "No home URL registered. Make sure one of your apps calls "
                "home_registry.register_home_url() in its ready() method."
            )

        try:
            return reverse(self._home_url_name)
        except Exception as e:
            raise ImproperlyConfigured(
                f"Could not reverse home URL '{self._home_url_name}' "
                f"registered by app '{self._home_app}': {e}"
            )

    def get_home_url_name(self):
        """Get the registered home URL name."""
        return self._home_url_name

    def get_home_app(self):
        """Get the app that registered the home URL."""
        return self._home_app

    def is_registered(self):
        """Check if a home URL is registered."""
        return self._registered

    def clear(self):
        """Clear the registered home URL (useful for testing)."""
        self._home_url_name = None
        self._home_app = None
        self._registered = False


# Global registry instance
home_registry = HomeURLRegistry()


# Convenience functions
def register_home_url(url_name, app_name):
    """Convenience function to register home URL."""
    return home_registry.register_home_url(url_name, app_name)


def get_home_url():
    """Convenience function to get home URL."""
    return home_registry.get_home_url()


def get_home_url_name():
    """Convenience function to get home URL name."""
    return home_registry.get_home_url_name()


if __name__ == "__main__":
    # ****************** Example Usage ******************

    print("=== Django Home URL Registry Example ===\n")

    # Example 1: Basic registration and retrieval
    print("1. Basic Registration Example:")
    print("-" * 30)

    # Register a home URL
    success = register_home_url("dashboard:index", "dashboard")
    print(f"Registration successful: {success}")
    print(f"Home URL name: {get_home_url_name()}")
    print(f"Registered by app: {home_registry.get_home_app()}")
    print(f"Is registered: {home_registry.is_registered()}")
    print()

    # Example 2: Attempt duplicate registration
    print("2. Duplicate Registration Example:")
    print("-" * 35)

    # Try to register another home URL (should fail)
    success2 = register_home_url("blog:home", "blog")
    print(f"Second registration successful: {success2}")
    print(f"Home URL name remains: {get_home_url_name()}")
    print(f"Still registered by: {home_registry.get_home_app()}")
    print()

    # Example 3: Clear and re-register
    print("3. Clear and Re-register Example:")
    print("-" * 34)

    # Clear the registry
    home_registry.clear()
    print(f"After clearing - Is registered: {home_registry.is_registered()}")

    # Register a new home URL
    success3 = register_home_url("blog:home", "blog")
    print(f"New registration successful: {success3}")
    print(f"New home URL name: {get_home_url_name()}")
    print(f"New registered app: {home_registry.get_home_app()}")
    print()

    # Example 4: Error handling
    print("4. Error Handling Example:")
    print("-" * 26)

    # Clear registry to demonstrate error
    home_registry.clear()
    print("Registry cleared. Attempting to get home URL without registration...")

    try:
        url = get_home_url()
        print(f"Home URL: {url}")
    except ImproperlyConfigured as e:
        print(f"Expected error: {e}")
    print()

    # Example 5: How to use in Django apps
    print("5. How to Use in Django Apps:")
    print("-" * 30)
    print("""
    # In your app's apps.py file:
    
    from django.apps import AppConfig
    from base.home import register_home_url
    
    class DashboardConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'dashboard'
        
        def ready(self):
            # Register this app's home URL
            register_home_url('dashboard:index', 'dashboard')
    
    # In your templates:
    
    {% load url %}
    <a href="{% url home_url_name %}">Home</a>
    
    # Or in your views:
    
    from base.home import get_home_url
    from django.shortcuts import redirect
    
    def some_view(request):
        # Redirect to home
        return redirect(get_home_url())
    
    # In your URL patterns:
    
    from base.home import get_home_url_name
    
    urlpatterns = [
        path('', RedirectView.as_view(url=get_home_url()), name='root'),
        # other patterns...
    ]
    """)

    print("=== Example Complete ===")
