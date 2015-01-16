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

        for page in pages:
            text=page.text()
            v=text.replace(r'//','&#47;').replace("[[","&#91;").replace("]]","&#93;")
            tokens=tokenizer.split(v)
            printed=False
            print page
            for token in tokens:
                if not token: continue
                if not token[0]=="[": continue
                if len(token)==1:
                    if not printed:
                        print page
                        printed=True
                    print "    wrong bracket"
                    continue
                if token[1]=="/": continue
                flag=( token[1:5] in [ "iurl","file" ] ) or  ( token[1:4] in [ "img" ] )
                if not flag: continue
                q=token.replace('[','').replace(']','')
                if q[-1]=="/": q=q[:-1]
                try:
                    x=shlex_split(q)
                except ValueError, e:
                    if not printed:
                        print page
                        printed=True
                    print "    wrong q:",q
                    continue
                args=x[1:]
                params={}
                if "=" in x[0]:
                    t=x[0].split('=')
                    tag=t[0]
                    params["name"]="=".join(t[1:])
                else:
                    tag=x[0]
                for arg in args:
                    t=arg.split("=")
                    if len(t)==1: continue
                    params[t[0]]='='.join(t[1:])
                if tag=="img":
                    if not params.has_key("name"):
                        params["name"]=params["img"]
                    if params.has_key("url"):
                        if not printed:
                            print page
                            printed=True
                        print "    image url:",url
                        continue
                    try:
                        image=Image.objects.get(name=params["name"])
                    except Image.DoesNotExist, e:
                        if not printed:
                            print page
                            printed=True
                        print "    internal image doesn't exist:",params["name"]
                    continue
                if tag=="iurl":
                    if not params.has_key("name"):
                        params["name"]=params["page"]
                    try:
                        pother=Page.objects.get(name=params["name"])
                    except Page.DoesNotExist, e:
                        if not printed:
                            print page
                            printed=True
                        print "    internal page doesn't exist:",params["name"]
                    continue
                if not params.has_key("name"):
                    if not printed:
                        print page
                        printed=True
                    print "    q:",q
                if tag=="file":
                    if params.has_key("url"):
                        if not printed:
                            print page
                            printed=True
                        print "    file url:",url
                        continue
                    try:
                        fname=File.objects.get(name=params["name"])
                    except File.DoesNotExist, e:
                        if not printed:
                            print page
                            printed=True
                        print "    internal file doesn't exist:",params["name"]
                    continue

            
