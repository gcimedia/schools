from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe

from ..models import BaseDetail, BaseImage

register = template.Library()


def load_base_config():
    """Fetch BaseDetail and BaseImage data from the database."""
    config = {
        **{f"{d.name}": d.value for d in BaseDetail.objects.only("name", "value")},
        **{
            i.name.lower(): i.image.url
            for i in BaseImage.objects.only("name", "image")
            if i.image
        },
    }
    return config


def get_base_config():
    """Return base config, using cache in production, always fresh in DEBUG."""
    if settings.DEBUG:
        return load_base_config()

    base_config = cache.get("base_config")
    if base_config is None:
        base_config = load_base_config()
        cache.set("base_config", base_config, 3600)

    return base_config


def get_base_detail(name, default=""):
    config = get_base_config()
    return config.get(name, default)


@register.simple_tag
def base_meta():
    """
    Render all standard meta tags as HTML using get_base_detail().
    Usage: {% base_meta %}
    """
    html = f"""
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <meta name="theme-color" content="{get_base_detail("base_theme_color", "#000")}" />
    <meta name="author" content="{get_base_detail("base_author")}" />
    <meta name="description" content="{get_base_detail("base_description")}" />
    <meta name="keywords" content="{get_base_detail("base_name")}" />
    
    <!-- Twitter -->
    <meta name="twitter:card" content="{get_base_detail("base_description")}" />
    <meta name="twitter:site" content="{get_base_detail("base_url")}" />
    <meta name="twitter:title" content="{get_base_detail("base_name")}" />
    <meta name="twitter:description" content="{get_base_detail("base_description")}" />
    <meta name="twitter:image" content="{get_base_detail("base_logo")}" />
    <meta name="twitter:image:alt" content="{get_base_detail("base_name")}" />
    
    <!-- Open Graph -->
    <meta property="og:url" content="{get_base_detail("base_url")}" />
    <meta property="og:site_name" content="{get_base_detail("base_name")}" />
    <meta property="og:title" content="{get_base_detail("base_name")}" />
    <meta property="og:image" content="{get_base_detail("base_logo")}" />
    <meta property="og:locale" content="en_GB" />
    """

    return mark_safe(html.strip())


@register.simple_tag(takes_context=True)
def base_title(context, title=None, separator=" | "):
    """
    Render the full HTML <title> tag with the page title and site name.
    Usage:
      - {% base_title %}                   ← uses context['base_title']
      - {% base_title "Custom Title" %}    ← uses provided title
      - {% base_title "Custom" " - " %}    ← uses custom separator
    """

    base_name = get_base_detail("base_name")

    if title is None:
        title = context.get("page_title")

    if title:
        full_title = f"{title}{separator}{base_name}"
    else:
        full_title = base_name

    return mark_safe(f"<title>{full_title}</title>")


@register.simple_tag
def base_icons():
    """
    Render <link> tags for the site's favicon and Apple touch icon.
    Usage: {% base_icons %}
    """

    favicon = get_base_detail("base_favicon")
    apple_icon = get_base_detail("base_apple_touch_icon")

    html = f"""
    <link rel="icon" type="image/x-icon" href="{favicon}">
    <link rel="apple-touch-icon" href="{apple_icon}">
    """

    return mark_safe(html.strip())


@register.simple_tag
def base_name():
    """Get org name specifically"""
    return get_base_detail("base_name")

@register.simple_tag
def base_short_name():
    """Get org name specifically"""
    return get_base_detail("base_short_name")


@register.simple_tag
def base_description():
    """Get org description specifically"""
    return get_base_detail("base_description")


@register.simple_tag
def base_logo():
    """Get org logo URL"""
    return get_base_detail("base_logo")


@register.simple_tag
def base_hero_image():
    """Get org logo URL"""
    return get_base_detail("base_hero_image")


@register.simple_tag
def base_credits():
    author = get_base_detail("base_author")
    author_url = get_base_detail("base_author_url")

    class_name = "pe-none" if not author_url or author_url == "#" else ""

    html = (
        f'Designed by <a href="{author_url}" class="{class_name}"><em>{author}</em></a>'
    )
    return mark_safe(html.strip())

