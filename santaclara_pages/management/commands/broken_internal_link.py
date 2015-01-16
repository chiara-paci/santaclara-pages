#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from santaclara_pages.models import Page,Image,File
from santaclara_editor.santaclara_lang.utility import shlex_split

class Command(BaseCommand):
    args = ''
    help = 'Broken internal link'

    def handle(self, *args, **options):
        pages=Page.objects.all()

        lab=r'[a-zA-Z0-9]+'
        args=r'[^\]\[]*?'
        tag=r'\[.*?\]'
        newline='[ \r\n]+'
        txt=r'[^\r\n\[\]]+'
        regexp=r"((?:\[.*?\])|(?:[\n\r ]+))"
        #regexp=r'('+tag+'|'+txt+'|'+newline+')'
        
        tokenizer=re.compile(regexp)

        for page in pages[2:5]:
            text=page.text()
            v=text.replace(r'//','&#47;').replace("[[","&#91;").replace("]]","&#93;")
            tokens=tokenizer.split(v)
            print page
            for token in tokens:
                if not token: continue
                if not token[0]=="[": continue
                if token[1]=="/": continue
                flag=( token[1:5] in [ "iurl","file" ] ) or  ( token[1:4] in [ "img" ] )
                if not flag: continue
                q=token.replace('[','').replace(']','')
                if q[-1]=="/": q=q[:-1]
                x=shlex_split(q)
                args=x[1:]
                params={}
                if "=" in x[0]:
                    t=x[0].split('=')
                    tag=t[0]
                    params["tag_first"]="=".join(t[1:])
                else:
                    tag=x[0]
                for arg in args:
                    t=arg.split("=")
                    if len(t)==1: continue
                    params[t[0]]='='.join(t[1:])
                if tag=="img":
                    if params.has_key("url"):
                        print "    image url:",url
                        continue
                    try:
                        image=Image.objects.get(name=params["tag_first"])
                    except Image.DoesNotExist, e:
                        print "    internal image doesn't exist:",params["tag_first"]
                        pass

                
                print token
            
