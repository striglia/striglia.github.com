#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Scott Triglia'
SITENAME = 'Locally Optimal'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

# Blogroll
LINKS = []

# Social widget
SOCIAL = [
	("Twitter", "http://www.twitter.com/scott_triglia"),
	("Github", "http://www.github.com/striglia"),
	("LinkedIn", "http://www.linkedin.com/in/striglia"),
]

PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['summary']
SUMMARY_END_MARKER = '<!-- more -->'


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

GOOGLE_ANALYTICS= 'UA-35190779-1'
