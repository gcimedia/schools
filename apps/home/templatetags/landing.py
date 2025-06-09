import logging

from django import template
from django.core.exceptions import ImproperlyConfigured

from ..config.landing import get_landing_url, get_landing_url_name, landing_config

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def landing_url():
    """
    Template tag to get the registered home URL.

    Usage:
        {% load landing %}
        <a href="{% landing_url %}">Home</a>
    """
    if not landing_config:
        logger.warning("Home registry not available")
        return "/"

    try:
        return get_landing_url()
    except ImproperlyConfigured:
        logger.warning("No home URL registered, falling back to '/'")
        return "/"


@register.simple_tag
def landing_url_name():
    """
    Template tag to get the registered home URL name.

    Usage:
        {% load landing %}
        <a href="{% url landing_url_name %}">Home</a>
    """
    if not landing_config:
        logger.warning("Home registry not available")
        return "home"

    try:
        return get_landing_url_name()
    except (ImproperlyConfigured, AttributeError):
        logger.warning("No home URL name registered, falling back to 'home'")
        return "home"


@register.simple_tag
def landing_url_with_fragment(fragment=None):
    """
    Template tag to get the home URL with an optional fragment.

    Usage:
        {% load landing %}
        <a href="{% landing_url_with_fragment 'hero' %}">Home</a>
        <a href="{% landing_url_with_fragment %}">Home</a>
    """
    if not landing_config:
        logger.warning("Home registry not available")
        base_url = "/"
    else:
        try:
            base_url = get_landing_url()
        except ImproperlyConfigured:
            logger.warning("No home URL registered, falling back to '/'")
            base_url = "/"

    if fragment:
        return f"{base_url}#{fragment}"
    return base_url


@register.filter
def is_landing_url(url_name):
    """
    Filter to check if a given URL name is the registered home URL.

    Usage:
        {% load landing %}
        {% if 'landing'|is_landing_url %}
            <span class="active">Current Home</span>
        {% endif %}
    """
    if not landing_config:
        return False

    try:
        registered_name = get_landing_url_name()
        return url_name == registered_name
    except (ImproperlyConfigured, AttributeError):
        return False


@register.simple_tag(takes_context=True)
def is_landing_page(context):
    """
    Template tag to check if the current page is the home page.

    Usage:
        {% load landing %}
        {% is_landing_page as is_home %}
        {% if is_home %}
            <div class="home-banner">Welcome to our homepage!</div>
        {% endif %}
    """
    request = context.get("request")
    if not request or not landing_config:
        return False

    try:
        landing_url = get_landing_url()
        current_path = request.path
        return current_path == landing_url
    except (ImproperlyConfigured, AttributeError):
        return False
