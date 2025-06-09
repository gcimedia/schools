class AuthConfig:
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
        # Global auth configuration
        self._global_config = {
            "username_field_label": "Username",
            "username_field_placeholder": "Enter your username",
        }

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

    def configure_username_field(self, label=None, placeholder=None):
        """Configure the username field globally."""
        if label is not None:
            self._global_config["username_field_label"] = label
        if placeholder is not None:
            self._global_config["username_field_placeholder"] = placeholder

    def get_username_config(self):
        """Get username field configuration."""
        return self._global_config.copy()

    def get_username_label(self):
        """Get the configured username field label."""
        return self._global_config["username_field_label"]

    def get_username_placeholder(self):
        """Get the configured username field placeholder."""
        return self._global_config["username_field_placeholder"]

    def set_global_config(self, **config):
        """Set global configuration options."""
        self._global_config.update(config)

    def get_global_config(self, key=None):
        """Get global configuration."""
        if key:
            return self._global_config.get(key)
        return self._global_config.copy()


# Global config instances
auth_config = AuthConfig()

# Example usage:
if __name__ == "__main__":
    # ****************** AuthPagesRegistry examples ******************
    print("=== AuthPagesRegistry Examples ===")

    # Configure username field globally
    auth_config.configure_username_field(
        label="Phone Number", placeholder="Your phone number"
    )

    # Set global configuration (multiple options at once)
    auth_config.set_global_config(
        username_field_label="Student ID",
        username_field_placeholder="Enter your student ID",
        password_min_length=8,
        require_email_verification=True,
        session_timeout=3600,
        max_login_attempts=5,
    )

    # Get specific global config value
    print("Username label:", auth_config.get_global_config("username_field_label"))
    print("Password min length:", auth_config.get_global_config("password_min_length"))

    # Get all global configuration
    print("All global config:", auth_config.get_global_config())

    # Enable/disable pages
    auth_config.enable_page("password_reset")
    auth_config.disable_page("signup")

    # Configure pages
    auth_config.configure_page("signin", redirect_url="/dashboard", require_2fa=True)
    auth_config.configure_page("profile_update", fields=["email", "name", "avatar"])

    # Bulk configuration
    auth_config.bulk_configure(
        {
            "signin": {"redirect_url": "/home", "remember_me": True},
            "signup": {"enabled": True, "require_email_verification": True},
            "email_verification": {"enabled": True, "expiry_hours": 24},
        }
    )

    # Check status
    print("Enabled pages:", auth_config.get_enabled_pages())
    print("Signin enabled:", auth_config.is_enabled("signin"))
    print("Signin config:", auth_config.get_page_config("signin"))
    print("Username label:", auth_config.get_username_label())
    print("Username placeholder:", auth_config.get_username_placeholder())

    # Get username configuration
    print("Username config:", auth_config.get_username_config())

    print("\nAll pages status:")
    for page, status in auth_config.get_all_pages_status().items():
        print(f"  - {page}: {'✓' if status['enabled'] else '✗'} {status['config']}")

    print("\n=== Global Configuration Examples ===")

    # Example 1: Configure for a school system
    auth_config.set_global_config(
        username_field_label="Student ID",
        username_field_placeholder="Enter your student ID",
        password_min_length=8,
        require_uppercase=True,
        require_numbers=True,
        allow_password_reset=True,
    )

    # Example 2: Configure for a phone-based system
    auth_config.set_global_config(
        username_field_label="Phone Number",
        username_field_placeholder="Your phone number",
        sms_verification=True,
        country_code_required=True,
    )

    # Example 3: Configure for an email-based system
    auth_config.set_global_config(
        username_field_label="Email Address",
        username_field_placeholder="your@email.com",
        email_verification_required=True,
        allow_social_login=True,
    )

    # Get specific configurations
    print(
        "Current username label:",
        auth_config.get_global_config("username_field_label"),
    )
    print(
        "Email verification required:",
        auth_config.get_global_config("email_verification_required"),
    )
    print("SMS verification:", auth_config.get_global_config("sms_verification"))

    # Get all global settings
    all_settings = auth_config.get_global_config()
    print("\nAll global settings:")
    for key, value in all_settings.items():
        print(f"  {key}: {value}")
