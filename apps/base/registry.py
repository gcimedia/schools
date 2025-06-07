# Base registry.py

class NavigationRegistry:
    def __init__(self):
        self._items = []

    def register(self, name, url_name, order=0, fragment=None, type="", **kwargs):
        self._items.append(
            {
                "name": name,
                "url_name": url_name,
                "order": order,
                "fragment": fragment,
                "type": type,
                **kwargs,
            }
        )

    def get_items(self):
        return sorted(self._items, key=lambda x: x["order"])


class AuthPagesRegistry:
    def __init__(self):
        self._enabled_pages = {
            "signin": True,
            "signup": True,
            "profile_update": True,
            "password_reset": False,
            "email_verification": False,
            "logout": True,
        }
        self._page_configs = {}

    def enable_page(self, page_name, **config):
        """Enable an auth page with optional configuration."""
        if page_name in self._enabled_pages:
            self._enabled_pages[page_name] = True
            if config:
                self._page_configs[page_name] = config
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def disable_page(self, page_name):
        """Disable an auth page."""
        if page_name in self._enabled_pages:
            self._enabled_pages[page_name] = False
            self._page_configs.pop(page_name, None)
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def is_enabled(self, page_name):
        """Check if an auth page is enabled."""
        return self._enabled_pages.get(page_name, False)

    def get_enabled_pages(self):
        """Get list of all enabled auth pages."""
        return [page for page, enabled in self._enabled_pages.items() if enabled]

    def get_page_config(self, page_name):
        """Get configuration for a specific page."""
        return self._page_configs.get(page_name, {})

    def configure_page(self, page_name, **config):
        """Configure an auth page without changing its enabled status."""
        if page_name in self._enabled_pages:
            self._page_configs[page_name] = config
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def get_all_pages_status(self):
        """Get status of all auth pages."""
        return {
            page: {"enabled": enabled, "config": self._page_configs.get(page, {})}
            for page, enabled in self._enabled_pages.items()
        }

    def bulk_configure(self, pages_config):
        """Configure multiple pages at once.

        Args:
            pages_config (dict): Dict with page names as keys and config dicts as values.
                               Use {"enabled": False} to disable a page.
        """
        for page_name, config in pages_config.items():
            if page_name not in self._enabled_pages:
                raise ValueError(f"Unknown auth page: {page_name}")

            if "enabled" in config:
                self._enabled_pages[page_name] = config["enabled"]
                config = {k: v for k, v in config.items() if k != "enabled"}

            if config:
                self._page_configs[page_name] = config


# Global registry instances
nav_registry = NavigationRegistry()
auth_pages_registry = AuthPagesRegistry()

# Example usage:
if __name__ == "__main__":
    # NavigationRegistry examples
    print("=== NavigationRegistry Examples ===")

    # Register navigation items
    nav_registry.register("Home", "home", order=1, icon="house")
    nav_registry.register("About", "about", order=3, type="page")
    nav_registry.register(
        "Dashboard", "dashboard", order=2, fragment="overview", requires_auth=True
    )
    nav_registry.register("Contact", "contact", order=4, type="page", external=True)
    nav_registry.register(
        "Admin", "admin", order=10, type="admin", permissions=["admin"]
    )

    # Get sorted navigation items
    nav_items = nav_registry.get_items()
    print("Navigation items (sorted by order):")
    for item in nav_items:
        print(f"  - {item['name']} ({item['url_name']}) - Order: {item['order']}")

    print("\nNavigation items with extra attributes:")
    for item in nav_items:
        extras = {
            k: v for k, v in item.items() if k not in ["name", "url_name", "order"]
        }
        if extras:
            print(f"  - {item['name']}: {extras}")

    print("\n" + "=" * 50 + "\n")

    # AuthPagesRegistry examples
    print("=== AuthPagesRegistry Examples ===")

    # Enable/disable pages
    auth_pages_registry.enable_page("password_reset")
    auth_pages_registry.disable_page("signup")

    # Configure pages
    auth_pages_registry.configure_page(
        "signin", redirect_url="/dashboard", require_2fa=True
    )
    auth_pages_registry.configure_page(
        "profile_update", fields=["email", "name", "avatar"]
    )

    # Bulk configuration
    auth_pages_registry.bulk_configure(
        {
            "signin": {"redirect_url": "/home", "remember_me": True},
            "signup": {"enabled": True, "require_email_verification": True},
            "email_verification": {"enabled": True, "expiry_hours": 24},
        }
    )

    # Check status
    print("Enabled pages:", auth_pages_registry.get_enabled_pages())
    print("Signin enabled:", auth_pages_registry.is_enabled("signin"))
    print("Signin config:", auth_pages_registry.get_page_config("signin"))
    print("\nAll pages status:")
    for page, status in auth_pages_registry.get_all_pages_status().items():
        print(f"  - {page}: {'✓' if status['enabled'] else '✗'} {status['config']}")
