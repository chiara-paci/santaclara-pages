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
            is_id=True
            try:
                page_id=int(self.args["page"])
            except ValueError, e:
                is_id=False
            try:
                if is_id:
                    page=Page.objects.get(id=page_id)
                else:
                    page=Page.objects.get(name__iexact=self.args["page"])
                url=page.get_absolute_url()
                hclass="validpagename"
            except Page.DoesNotExist, e:
                url=""
                hclass="invalidpagename"
        S='<a href="'+url+'" class="'+hclass+'">'
        S+=tags.Tag.output(self,autoescape,outtype)
        S+="</a>"
        return(S)

santaclara_editor.languages.language_register.add_tag("iurl",factories.mk_class_tag(IUrlTag))

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
                    image=Image.objects.get(name__iexact=name)
                    url=image.path.replace(self.media_root,"")
                    if not caption:
                        caption=image.description
                except Image.DoesNotExist, e:
                    pass
        if url:
            url=self.media_url+url
        self.args["url"]=url
        if (not self.args["caption"]) and caption:
            self.args["caption"]=caption
        self.args["caption"]=self.lang.get_tags(self.args["caption"])

    def output(self,autoescape,outtype="html"):
        S='<div class="imagebox"><div class="image"><img src="'+self.args["url"]+'"/>'
        if self.args["caption"]:
            S+='<div class="caption">'
            print "CAPTION",type(self.args["caption"][0])
            if type(self.args["caption"][0])==unicode:
                par=tags.ParagraphTag(self.lang,None)
                par.add(self.args["caption"][0])
                self.args["caption"][0]=par
            span=tags.SpanTag(self.lang,None,"title")
            span.add("Fig. %d" % self.ind)
            self.args["caption"][0].insert(0,span)
            for t in self.args["caption"]:
                print "t",t
                S+=t.output(autoescape)
            S+="</div>"
        else:
            S+='<div class="caption"><span class="title">Fig. %d</span></div>' % (self.ind,)
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

santaclara_editor.languages.language_register.add_tag("img",mk_img_tag())

class FileTag(tags.Tag):
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
                    f=File.objects.get(name__iexact=name)
                    url=f.path.replace(self.media_root,"")
                    if not caption:
                        caption=f.description
                except File.DoesNotExist, e:
                    pass
        if url:
            url=self.media_url+url
        self.args["url"]=url
        if (not self.args["caption"]) and caption:
            self.args["caption"]=caption
        self.args["caption"]=self.lang.get_tags(self.args["caption"])

    def output(self,autoescape,outtype="html"):
        S='<a href="'+self.args["url"]+'">'
        if self.args["caption"]:
            for t in self.args["caption"]:
                x=t.output(autoescape)
                if x[0:3]=="<p>":
                    x=x[3:-4]
                S+=x
        else:
            S+=self.args["url"]
        S+="</a>"
        return(S)

class mk_file_tag(object):
    def __init__(self):
        self.ind=0

    def reset(self): self.ind=0

    def __call__(self,lang,padre):
        self.ind+=1
        return(FileTag(lang,padre,self.ind,settings.MEDIA_ROOT,settings.MEDIA_URL))

santaclara_editor.languages.language_register.add_tag("file",mk_file_tag())
