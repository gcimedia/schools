from django import template

from ..forms import ContactForm

register = template.Library()


@register.simple_tag
def contact_form(field):
    """Contact Form"""

    form = ContactForm()
    return form[field]
