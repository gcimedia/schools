from apps.base.registry import auth_pages_registry

# Disable the signup page for elearning app
auth_pages_registry.disable_page("signup")
