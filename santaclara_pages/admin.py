from django.contrib import admin
from django import forms

# Register your models here.
from santaclara_pages.models import Menu,MenuSubMenuRelation,MenuObject,MenuSeparator,MenuItem,MenuTitle
from santaclara_pages.models import Page,PageMenuRelation,MenuItemInternal,MenuTitleInternal,File,Image
from santaclara_pages.models import Scheda,SchedaValue,SchedaKey
from santaclara_base.admin import VersionedObjectAdmin,VersionInline

class MenuItemInternalForm(forms.ModelForm):
    text = forms.CharField(required=False,initial="")

    class Meta:
        model = MenuItemInternal

    def clean(self):
        cleaned_data=super(MenuItemInternalForm,self).clean()
        if not cleaned_data["text"]:
            cleaned_data["text"]=cleaned_data["page"].title
        return cleaned_data

class MenuItemInternalAdmin(admin.ModelAdmin):
    form=MenuItemInternalForm

class MenuTitleInternalForm(forms.ModelForm):
    text = forms.CharField(required=False,initial="")

    class Meta:
        model = MenuTitleInternal

    def clean(self):
        cleaned_data=super(MenuTitleInternalForm,self).clean()
        if not cleaned_data["text"]:
            cleaned_data["text"]=cleaned_data["page"].title
        return cleaned_data

class MenuTitleInternalAdmin(admin.ModelAdmin):
    form=MenuTitleInternalForm

admin.site.register(MenuSubMenuRelation)
admin.site.register(MenuSeparator)
admin.site.register(MenuItem)
admin.site.register(MenuItemInternal,MenuItemInternalAdmin)
admin.site.register(MenuTitleInternal,MenuTitleInternalAdmin)
admin.site.register(MenuTitle)

class SchedaValueInline(admin.TabularInline):
    model = SchedaValue
    extra = 0

class SchedaAdmin(admin.ModelAdmin):
    inlines = [SchedaValueInline]

admin.site.register(Scheda,SchedaAdmin)
admin.site.register(SchedaKey)
admin.site.register(SchedaValue)

class ImageAdmin(admin.ModelAdmin):
    list_display=('name','path')

admin.site.register(Image,ImageAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display=('name','path')

admin.site.register(File,FileAdmin)

class MenuObjectAdmin(admin.ModelAdmin):
    list_display=('__unicode__','parent','pos','content_type',)

admin.site.register(MenuObject,MenuObjectAdmin)

class MenuObjectInline(admin.TabularInline):
    model = MenuObject
    extra = 0
    ordering = ['pos']
    max_num = 0

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    ordering = ['pos']


class MenuItemInternalInline(admin.TabularInline):
    model = MenuItemInternal
    extra = 0
    ordering = ['pos']
    form = MenuItemInternalForm


class MenuTitleInternalInline(admin.TabularInline):
    model = MenuTitleInternal
    extra = 0
    ordering = ['pos']
    form = MenuTitleInternalForm

class MenuSeparatorInline(admin.TabularInline):
    model = MenuSeparator
    extra = 0
    ordering = ['pos']

class MenuTitleInline(admin.TabularInline):
    model = MenuTitle
    extra = 0
    ordering = ['pos']

class SubMenuInline(admin.TabularInline):
    model = MenuSubMenuRelation
    extra = 0
    fk_name = 'parent'

class MenuAdmin(admin.ModelAdmin):
    inlines=(SubMenuInline,MenuObjectInline,MenuTitleInternalInline,MenuTitleInline,MenuItemInternalInline,MenuItemInline,MenuSeparatorInline)
    save_on_top=True

admin.site.register(Menu,MenuAdmin)

class PageMenuInline(admin.TabularInline):
    model = PageMenuRelation
    extra = 0

class SchedaInline(admin.TabularInline):
    model = Scheda
    extra = 0

class PageAdmin(VersionedObjectAdmin):
    list_display=("name","title","has_toc")
    inlines = (SchedaInline,PageMenuInline,VersionInline)

admin.site.register(Page,PageAdmin)
admin.site.register(PageMenuRelation)
