from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from .registry.auth import auth_registry
from .registry.landing import get_landing_url_name


def auth_page_required(page_name):
    """Simple decorator that blocks all access when page is disabled."""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not auth_registry.is_enabled(page_name):
                # For API requests
                if (
                    request.headers.get("Content-Type") == "application/json"
                    or request.headers.get("X-Requested-With") == "XMLHttpRequest"
                ):
                    return JsonResponse(
                        {"error": f"{page_name} is currently unavailable."}, status=403
                    )

                # For regular requests
                messages.warning(
                    request,
                    f"{page_name.title()} is currently unavailable.",
                    extra_tags="auth_page_required",
                )
                return redirect(get_landing_url_name())
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def auth_page_required_class(page_name):
    """Decorator for class-based views."""

    def decorator(cls):
        # Apply the decorator to the dispatch method
        cls.dispatch = method_decorator(auth_page_required(page_name))(cls.dispatch)
        return cls

    return decorator
