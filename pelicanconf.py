#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Admin'
SITENAME = u'One Salon'
TIMEZONE = 'America/Los_Angeles'
SITEURL = ''

PATH = 'content'
THEME = '.'
STATIC_PATHS = ['extra']
USE_FOLDER_AS_CATEGORY = True

ARTICLE_URL = PAGE_URL = '{slug}'
ARTICLE_SAVE_AS = PAGE_SAVE_AS = '{slug}/index.html'

DEFAULT_PAGINATION = False
TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = u'en'

FEED_RSS = None
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
FEED_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
 
DIRECT_TEMPLATES = ['index']
# Blogroll
LINKS = []
SOCIAL = []

ARTICLE_ORDER_BY = 'sort'
PAGE_ORDER_BY = 'sort'


EXTRA_PATH_METADATA = {
    'extra/'+p: {'path': p} for p in os.listdir('content/extra')
}

if os.environ.get('CONFIG') == 'production':
    SITEURL = 'http://www.onesalon.org'
    RELATIVE_URLS = False

    DELETE_OUTPUT_DIRECTORY = True

    #GOOGLE_ANALYTICS = "UA-67530965-1"
    #VERIFY_CODE = 'bmy3nuQW4emYXaZlchSU3HxMcor52beaXkLmCS6uTVo'
