from django.db import models
from django.conf import settings
from django.utils.safestring import SafeUnicode

from santaclara_base.models import PositionAbstract
from santaclara_base.models import VersionedAbstract
from santaclara_base.models import DefaultUrl

from django.contrib.contenttypes.models import ContentType

import santaclara_base.utility

# Create your models here.

class Copyright(models.Model):
    short_name = models.CharField(max_length=2048,unique=True)
    long_name = models.CharField(max_length=2048,blank=True)
    logo_html = models.CharField(max_length=2048,blank=True)
    url = models.CharField(max_length=2048,blank=True)

    def __unicode__(self):
        return unicode(self.long_name)

    def logo(self): 
        return SafeUnicode(self.logo_html)

class Menu(models.Model):
    name = models.CharField(max_length=2048,unique=True)
    sub_menus = models.ManyToManyField("self",symmetrical=False,through="MenuSubMenuRelation")

    def __unicode__(self): return(self.name)

    def get_items(self):
        L=[]
        for submenu in self.child_set.all():
            for pos,mtype,obj in submenu.child.get_items():
                L.append( ([submenu.pos]+pos,mtype,obj) )
        L+=map(lambda o: ([o.pos],unicode(o.content_type),o.actual()),
               self.menuobject_set.all())
        L.sort()
        return L

    def next_pos(self): 
        last=list(self.menuobject_set.order_by('pos'))[-1]
        return last.pos+1

class MenuSubMenuRelation(PositionAbstract):
    parent = models.ForeignKey(Menu,related_name='child_set')
    child = models.ForeignKey(Menu,related_name='parent_set')

    def __unicode__(self): 
        return(unicode(self.parent)+"/"+unicode(self.child))

class MenuObject(PositionAbstract):
    parent = models.ForeignKey(Menu)
    content_type = models.ForeignKey(ContentType,editable=False,blank=True,null=True)

    class Meta:
        ordering = ['pos']

    def type(self):
        return unicode(self.content_type)

    def actual(self):
        model = self.content_type.model
        return self.__getattribute__(model)

    def __unicode__(self):
        try:
            return self.actual().__unicode__()
        except:
            return(unicode(self.pos))
    __unicode__.admin_order_field = 'pos'

    def save(self, *args, **kwargs):
        if (not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(MenuObject, self).save(*args, **kwargs)

class MenuSeparator(MenuObject): 
    def __unicode__(self): return "sep"

class MenuItem(MenuObject):
    level = models.IntegerField(default=0,choices=[ (0,"base"),(1,"under h1"), (2,"under h2"), (3,"under h3") ])
    text = models.CharField(max_length=2048)
    url = models.CharField(max_length=4096,blank=True)

    def __unicode__(self): return(unicode(self.text))

class MenuTitle(MenuObject):
    level = models.IntegerField(default=1,choices=[ (1,"h1"), (2,"h2"), (3,"h3") ])
    text = models.CharField(max_length=2048)
    url = models.CharField(max_length=4096,blank=True)

    def __unicode__(self): return("h"+unicode(self.level)+": "+unicode(self.text))


class Page(VersionedAbstract,DefaultUrl): 
    name = models.CharField(max_length=1024,unique=True)
    title = models.CharField(max_length=2048,blank=True,default="")
    has_toc = models.BooleanField(default=True)
    num_columns = models.PositiveIntegerField(default=1)
    menus = models.ManyToManyField(Menu,through="PageMenuRelation")
    copyright = models.ForeignKey(Copyright,default=1)
    visible = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType,editable=False,blank=True,null=True)

    class Meta:
        ordering = [ "name","title" ]

    def type(self):
        return unicode(self.content_type)

    def actual(self):
        model = self.content_type.model
        return self.__getattribute__(model)

    def __unicode__(self): 
        return unicode(self.name)
        # if self.title:
        #     return unicode(self.title)
        # else:
        #     return "["+unicode(self.name)+"]"

    def get_absolute_url(self):
        try:
            return self.actual().get_absolute_url()
        except:
            return DefaultUrl.get_absolute_url(self)

    def save(self, *args, **kwargs):
        if (not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Page, self).save(*args, **kwargs)

class PageMenuRelation(PositionAbstract):
    page = models.ForeignKey(Page)
    menu = models.ForeignKey(Menu)

    def __unicode__(self): 
        return(unicode(self.page)+"/"+unicode(self.menu))

    class Meta:
        ordering = ['pos']

class MenuItemInternal(MenuObject):
    level = models.IntegerField(default=0,choices=[ (0,"under h1 (base)"),(1,"under h2"), (2,"under h3")])
    text = models.CharField(max_length=2048)
    page = models.ForeignKey(Page)

    def __unicode__(self): return(unicode(self.text))

class MenuTitleInternal(MenuObject):
    level = models.IntegerField(default=1,choices=[ (1,"h1"), (2,"h2"), (3,"h3") ])
    text = models.CharField(max_length=2048)
    page = models.ForeignKey(Page)

    def __unicode__(self): return("h"+unicode(self.level)+": "+unicode(self.text))

class File(models.Model): 
    name = models.CharField(max_length=1024,unique=True)
    description = models.TextField()
    path = models.FilePathField(max_length=2048,path=settings.MEDIA_ROOT+"/files/",allow_folders=True)

    def __unicode__(self): 
        return unicode(self.name)

class Image(models.Model): 
    name = models.CharField(max_length=1024,unique=True)
    description = models.TextField()
    alternate = models.CharField(max_length=2048)
    path = models.FilePathField(max_length=2048,path=settings.MEDIA_ROOT+"/images/",allow_folders=True)

    def __unicode__(self): 
        return unicode(self.name)

    def url(self):
        return self.path.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)

class Icon(models.Model): 
    name = models.CharField(max_length=1024,unique=True)
    description = models.TextField()
    alternate = models.CharField(max_length=2048)
    path = models.FilePathField(max_length=2048,path=settings.MEDIA_ROOT+"/icons/",allow_folders=True)

    def __unicode__(self): 
        return unicode(self.name)

    def url(self):
        return self.path.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)

class SchedaKey(models.Model):
    name = models.CharField(max_length=1024,unique=True)

    def __unicode__(self):
        return unicode(self.name)

class Scheda(models.Model):
    page = models.ForeignKey(Page)
    name = models.CharField(max_length=1024,unique=True)
    values = models.ManyToManyField(SchedaKey,through="SchedaValue")

    def __unicode__(self):
        return unicode(self.name)

class SchedaValue(models.Model):
    key = models.ForeignKey(SchedaKey)
    scheda = models.ForeignKey(Scheda)
    value = models.CharField(max_length=4096)

    def __unicode__(self):
        return unicode(self.key)+": "+unicode(self.value)
    
class FooterSection(PositionAbstract):
    menu = models.ForeignKey(Menu)

    class Meta:
        ordering = [ "pos" ]

    def __unicode__(self): 
        return unicode(self.menu)

class HomeSection(PositionAbstract):
    label = models.SlugField(unique=True)

    class Meta:
        ordering = [ "pos" ]

    def __unicode__(self): 
        return unicode(self.label)
    
class HomeBlock(PositionAbstract):
    section = models.ForeignKey(HomeSection)
    image_url = models.CharField(max_length=2048,blank=True)
    image_alt = models.CharField(max_length=2048,blank=True)
    title = models.CharField(max_length=2048)
    page = models.ForeignKey(Page)
    num_words = models.IntegerField(default=60)
    valid = models.BooleanField(default=True)

    class Meta:
        ordering = [ "pos" ]

    def __unicode__(self): 
        return unicode(self.title)
    
