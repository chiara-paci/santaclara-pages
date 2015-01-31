from django import template
from santaclara_pages.models import Page,Image,File

register = template.Library()

def get_by_id_or_name(model,key):
    is_id=True
    try:
        obj_id=int(key)
    except ValueError, e:
        is_id=False
    try:
        if is_id:
            obj=model.objects.get(id=obj_id)
        else:
            obj=model.objects.get(name=key)
    except model.DoesNotExist:
        return None
    return obj

@register.simple_tag
def page_url(name):
    page=get_by_id_or_name(Page,name)
    if not page:
        return ""
    return page.get_absolute_url()

@register.simple_tag
def page_class(name):
    page=get_by_id_or_name(Page,name)
    if not page:
        return "invalidpagename"
    return "validpagename"

@register.simple_tag
def image_url(name):
    image=get_by_id_or_name(Image,name)
    if not image:
        return ""
    return image.url()

@register.simple_tag
def image_class(name):
    image=get_by_id_or_name(Image,name)
    if not image:
        return "invalidimagename"
    return "validimagename"

@register.simple_tag
def image_description(name):
    image=get_by_id_or_name(Image,name)
    if not image:
        return ""
    return unicode(image.description)

@register.simple_tag
def image_alt(name):
    image=get_by_id_or_name(Image,name)
    if not image:
        return ""
    return unicode(image.alternate)

@register.simple_tag
def file_url(name):
    fobj=get_by_id_or_name(File,name)
    if not fobj:
        return ""
    return fobj.url()

@register.simple_tag
def file_class(name):
    fobj=get_by_id_or_name(File,name)
    if not fobj:
        return "invalidfilename"
    return "validfilename"

@register.simple_tag
def file_description(name):
    fobj=get_by_id_or_name(File,name)
    if not fobj:
        return ""
    return unicode(fobj.description)

