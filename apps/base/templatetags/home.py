import logging

from django import template
from django.core.exceptions import ImproperlyConfigured

from ..registry.home import get_home_url, get_home_url_name, home_registry

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def home_url():
    """
    Template tag to get the registered home URL.

    Usage:
        {% load home %}
        <a href="{% home_url %}">Home</a>
    """
    if not home_registry:
        logger.warning("Home registry not available")
        return "/"

    try:
        return get_home_url()
    except ImproperlyConfigured:
        logger.warning("No home URL registered, falling back to '/'")
        return "/"


@register.simple_tag
def home_url_name():
    """
    Template tag to get the registered home URL name.

    Usage:
        {% load home %}
        <a href="{% url home_url_name %}">Home</a>
    """
    if not home_registry:
        logger.warning("Home registry not available")
        return "home"

    try:
        return get_home_url_name()
    except (ImproperlyConfigured, AttributeError):
        logger.warning("No home URL name registered, falling back to 'home'")
        return "home"


@register.simple_tag
def home_url_with_fragment(fragment=None):
    """
    Template tag to get the home URL with an optional fragment.

    Usage:
        {% load home %}
        <a href="{% home_url_with_fragment 'hero' %}">Home</a>
        <a href="{% home_url_with_fragment %}">Home</a>
    """
    if not home_registry:
        logger.warning("Home registry not available")
        base_url = "/"
    else:
        try:
            base_url = get_home_url()
        except ImproperlyConfigured:
            logger.warning("No home URL registered, falling back to '/'")
            base_url = "/"

    if fragment:
        return f"{base_url}#{fragment}"
    return base_url


@register.filter
def is_home_url(url_name):
    """
    Filter to check if a given URL name is the registered home URL.

    Usage:
        {% load home %}
        {% if 'landing:home'|is_home_url %}
            <span class="active">Current Home</span>
        {% endif %}
    """
    if not home_registry:
        return False

    try:
        registered_name = get_home_url_name()
        return url_name == registered_name
    except (ImproperlyConfigured, AttributeError):
        return False


@register.simple_tag(takes_context=True)
def is_home_page(context):
    """
    Template tag to check if the current page is the home page.

    Usage:
        {% load home %}
        {% is_home_page as is_home %}
        {% if is_home %}
            <div class="home-banner">Welcome to our homepage!</div>
        {% endif %}
    """
    request = context.get("request")
    if not request or not home_registry:
        return False

    try:
        home_url = get_home_url()
        current_path = request.path
        return current_path == home_url
    except (ImproperlyConfigured, AttributeError):
        return False
