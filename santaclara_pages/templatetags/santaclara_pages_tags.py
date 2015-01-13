from django import template
from santaclara_pages.models import Page

register = template.Library()

@register.simple_tag
def page_url(name):
    try:
        page=Page.objects.get(name=name)
    except Page.DoesNotExist:
        return name
    return page.get_absolute_url()
