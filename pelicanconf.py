#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Scott Triglia'
SITENAME = 'Locally Optimal'
SITEURL = 'http://locallyoptimal.com'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'
SITESUBTITLE = 'hill climbing in SF';

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

STATIC_PATHS = ['extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

PLUGIN_PATHS = ['/Users/striglia/Desktop/github/pelican-plugins']
PLUGINS = ['summary', 'gravatar']
SUMMARY_END_MARKER = '<!-- more -->'
AUTHOR_EMAIL = 'scott.triglia@gmail.com'
PELICAN_SOBER_TWITTER_CARD_CREATOR = 'scott_triglia'
PELICAN_SOBER_STICKY_SIDEBAR = True

THEME = "/Users/striglia/Desktop/github/pelican-themes/pelican-sober"
PELICAN_SOBER_ABOUT = "I'm Scott Triglia 👋 I mostly write here about software, technical leadership, and public speaking."

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Add line numbers to code blocks
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

