#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
import os
import sys
import site

site.addsitedir('/home/userweb/.virtualenvs/sibotero/lib/python2.7/site-packages/')
sys.path.append('/home/userweb/SiBotero')
#os.environ['PYTHON_EGG_CACHE'] = '/var/django/cache'

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE']='SiCoBotero.settings'
application = WSGIHandler()
