from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def vendor_bootstrap():
    html = f"""
    <link rel="stylesheet" href="{static("home/vendor/bootstrap/css/bootstrap.min.css")}"/>
    <script defer src="{static("home/vendor/bootstrap/js/bootstrap.bundle.min.js")}"></script>
    """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_bootstrap_icons():
    html = f"""
    <link rel="stylesheet" href="{static("home/vendor/bootstrap-icons/bootstrap-icons.min.css")}"/>
    """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_aos():
    html = f"""
    <link rel="stylesheet" href="{static("home/vendor/aos/aos.css")}"/>
    <link rel="stylesheet" href="{static("home/vendor/aos/init.css")}"/>
    <script defer src="{static("home/vendor/aos/aos.js")}"></script>
    <script defer src="{static("home/vendor/aos/init.js")}"></script>
    """

    return mark_safe(html.strip())
