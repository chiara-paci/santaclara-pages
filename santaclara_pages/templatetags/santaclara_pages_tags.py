from django import template
from santaclara_pages.models import Page,Image,File

register = template.Library()

@register.simple_tag
def page_url(name):
    is_id=True
    try:
        page_id=int(name)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            page=Page.objects.get(id=page_id)
        else:
            page=Page.objects.get(name=name)
    except Page.DoesNotExist:
        return ""
    return page.get_absolute_url()

@register.simple_tag
def page_class(name):
    is_id=True
    try:
        page_id=int(name)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            page=Page.objects.get(id=page_id)
        else:
            page=Page.objects.get(name=name)
    except Page.DoesNotExist:
        return "invalidpagename"
    return "validpagename"

@register.simple_tag
def image_url(name):
    is_id=True
    try:
        image_id=int(name)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            image=Image.objects.get(id=image_id)
        else:
            image=Image.objects.get(name=name)
    except Image.DoesNotExist:
        return ""
    return image.url()

@register.simple_tag
def image_class(name):
    is_id=True
    try:
        image_id=int(name)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            image=Image.objects.get(id=image_id)
        else:
            image=Image.objects.get(name=name)
    except Image.DoesNotExist:
        return "invalidimagename"
    return "validimagename"

@register.simple_tag
def file_url(name):
    is_id=True
    try:
        file_id=int(name)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            file=File.objects.get(id=file_id)
        else:
            file=File.objects.get(name=name)
    except File.DoesNotExist:
        return ""
    return file.url()

@register.simple_tag
def file_class(name):
    is_id=True
    try:
        file_id=int(name)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            file=File.objects.get(id=file_id)
        else:
            file=File.objects.get(name=name)
    except File.DoesNotExist:
        return "invalidfilename"
    return "validfilename"
