#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from santaclara_pages.models import Page

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
            for token in tokens:
                if not token: continue
                if not token[0]=="[": continue
                if token[1]=="/": continue
                flag=( token[1:5] in [ "iurl","file" ] ) or  ( token[1:4] in [ "img" ] )
                if not flag: continue
                print token
            
