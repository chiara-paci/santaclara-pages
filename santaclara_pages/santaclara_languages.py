from django.conf import settings

import santaclara_editor.languages

from santaclara_editor.santaclara_lang import tags
from santaclara_editor.santaclara_lang import factories

from santaclara_pages.models import Page,Image,File

import re

class IUrlTag(tags.Tag):
    def __init__(self,lang,padre):
        tags.Tag.__init__(self,lang,padre)

    def set_args(self,args):
        tags.Tag.set_args(self,args)
        if not self.args.has_key("page"):
            self.args["page"]=""
            if len(self.args)>=1:
                t=self.args[0].split("=")
                if len(t)>1:
                    self.args["page"]=t[1]

    def output(self,autoescape,outtype="html"):
        print "P",self.args["page"]
        if not self.args["page"]:
            url=""
        else:
            try:
                page=Page.objects.get(name=self.args["page"])
                url=page.get_absolute_url()
            except Page.DoesNotExist, e:
                url=""
        S='<a href="'+url+'">'
        S+=tags.Tag.output(self,autoescape,outtype)
        S+="</a>"
        return(S)

class ImgTag(tags.Tag):
    def __init__(self,lang,padre,ind,media_root,media_url):
        tags.Tag.__init__(self,lang,padre,inline=False)
        self.ind=ind
        self.media_root=media_root
        self.media_url=media_url

    def set_args(self,args):
        tags.Tag.set_args(self,args)
        if not self.args.has_key("caption"):
            caption=""
            self.args["caption"]=""
        else:
            caption=self.args["caption"]
        url=""
        if not self.args.has_key("url"):
            name=self.args[0].split("=")[1]
            if name:
                try:
                    image=Image.objects.get(name=name)
                    url=image.path.replace(self.media_root,"")
                    if not caption:
                        caption=image.description
                except Image.DoesNotExist, e:
                    pass
        if url:
            url=self.media_url+url
        self.args["url"]=url
        if not self.args["caption"] and caption:
            self.args["caption"]=self.lang.get_tags(caption)

    def output(self,autoescape,outtype="html"):
        S='<div class="imagebox"><div class="image"><img src="'+self.args["url"]+'"/>'
        if self.args["caption"]:
            S+='<div class="caption">'
            if type(self.args["caption"][0])==tags.ParagraphTag:
                span=tags.SpanTag(self.lang,None,"title")
                span.add("Fig. %d. " % self.ind)
                self.args["caption"][0].insert(0,span)
            else:
                span.padre=self
                S+=span.output(autoescape)
            for t in self.args["caption"]:
                S+=t.output(autoescape)
            S+="</div>"
        else:
            S+='<div class="caption"><span class="title">Fig. %d.</span></div>' % (self.ind,)
        S+='</div>'
        S+='</div>'
        return(S)

class mk_img_tag(object):
    def __init__(self):
        self.ind=0

    def reset(self): self.ind=0

    def __call__(self,lang,padre):
        self.ind+=1
        return(ImgTag(lang,padre,self.ind,settings.MEDIA_ROOT,settings.MEDIA_URL))

santaclara_editor.languages.language_register.add_tag("iurl",factories.mk_class_tag(IUrlTag))
santaclara_editor.languages.language_register.add_tag("img",mk_img_tag())

