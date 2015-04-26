#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Admin'
SITENAME = u'One Salon'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

PAGE_URL = PAGE_SAVE_AS = '{slug}.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing

if os.environ.get('ENV') == 'production':
    SITEURL = 'http://www.onesalon.org'
    RELATIVE_URLS = False

    DELETE_OUTPUT_DIRECTORY = True

    # Following items are often useful when publishing

    #DISQUS_SITENAME = ""
    #GOOGLE_ANALYTICS = ""
