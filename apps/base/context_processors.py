# Base context_processors.py

from django.urls import NoReverseMatch, reverse

from .registry import auth_pages_registry, nav_registry


def header(request):
    return {
        "show_header": True,
        "header_logo": True,
        "header_navigation": True,
        "header_auth_btn": True,
    }


def hero(request):
    return {
        "show_hero": False,
        "hero_btn_1": True,
        "hero_btn_1_login_required": False,
        "hero_btn_1_icon": "",
        "hero_btn_1_name": "Dashboard",
        "hero_btn_1_url_path": "/dashboard/",
        "hero_btn_2": False,
        "hero_btn_2_login_required": False,
        "hero_btn_2_icon": "",
        "hero_btn_2_name": "",
        "hero_btn_2_url_path": "",
    }


def auth(request):
    return {
        "show_auth": False,
        "auth_sigin": False,
        "auth_signup": False,
    }


def footer(request):
    return {
        "show_footer": True,
        "footer_newsletter": True,
        "footer_top": True,
        "footer_copyright": True,
    }


def overlay(request):
    return {
        "overlay_back_to_top": True,
        "overlay_whatsapp_call_us": True,
        "overlay_preloader": True,
    }


def registry(request):
    """Combined context processor for both navigation and auth pages."""

    # Navigation items
    nav_items = []
    for item in nav_registry.get_items():
        try:
            url = reverse(item["url_name"])
            if item.get("fragment"):
                url += f"#{item['fragment']}"

            nav_items.append(
                {
                    "name": item["name"],
                    "url": url,
                    "type": item.get("type", ""),
                }
            )
        except NoReverseMatch:
            continue

    # Auth pages
    enabled_pages = auth_pages_registry.get_enabled_pages()

    # Build auth URLs dictionary
    auth_urls = {}
    auth_configs = {}

    url_mappings = {
        "signin": "base:signin",
        "signup": "base:signup",
        "logout": "base:signout",  # Note: logout maps to signout
        "profile_update": "base:profile",  # Adjust if different
        "password_reset": "base:password_reset",  # Adjust if different
        "email_verification": "base:email_verify",  # Adjust if different
    }

    # Build URLs for enabled pages
    for page_name in enabled_pages:
        url_name = url_mappings.get(page_name)
        if url_name:
            try:
                auth_urls[page_name] = reverse(url_name)
                auth_configs[page_name] = auth_pages_registry.get_page_config(page_name)
            except NoReverseMatch:
                # Skip if URL pattern doesn't exist
                continue

    # Helper functions for templates
    auth_helpers = {
        "has_signin": auth_pages_registry.is_enabled("signin"),
        "has_signup": auth_pages_registry.is_enabled("signup"),
        "has_logout": auth_pages_registry.is_enabled("logout"),
        "has_profile_update": auth_pages_registry.is_enabled("profile_update"),
        "has_password_reset": auth_pages_registry.is_enabled("password_reset"),
        "has_email_verification": auth_pages_registry.is_enabled("email_verification"),
    }

    return {
        # Navigation context
        "nav_items": nav_items,
        # Auth pages context
        "auth_urls": auth_urls,
        "auth_configs": auth_configs,
        "auth_pages": auth_helpers,
        "enabled_auth_pages": enabled_pages,
    }
