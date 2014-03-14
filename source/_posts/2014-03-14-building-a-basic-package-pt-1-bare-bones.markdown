---
layout: post
title: "Building a basic package pt. 1: Bare Bones"
date: 2014-03-14 13:44
comments: true
categories: python packaging rss2sms
---

Every once in a while I get the itch to turn some one off script I wrote into a proper package. Turns out advice on the subject is a little scattered, and if you're anything like me it can be frustrating to track down relevant posts on the entire subject. So, just for fun, let's walk through the process of taking a one-off script I wrote and making it into a nice python package, complete with isolated testing, uploading to pypi, and convenient installation.

Now knowing my blogging habits, I'm splitting this into a few small posts in the hopes that I actually get through them. So lets take a current project I have and decide where to start.

<!-- more -->

## rss2sms - a humble beginning

The project I'd like to fix up is called rss2sms and lives [on my github account](http://www.github.com/striglia/rss2sms). I originally started it back when I was house hunting in San Francisco and was getting tired of new apartments going up on Craigslist without me noticing. So I figured it was time to automate this!

The code is pretty simple. At its core, it does the following steps whenever it is run:

1. Reads a passed RSS feed into memory (e.g. a Craigslist search)
2. Loads the timestamp of the last post we were notified about from file
3. Sends a text for each post newer than the timestamp to a specified number

As a result of being fairly simple, I just threw the whole thing in one python module. In fact, I threw it in one big class! I want to clean up the implementation a little as we go on, but for now let's focus on the task of turning this into a package.

## Structure

One of the easiest steps we can take toward making a package is to imitate the proper directory structure. The kind folks over at the Python Packaging Authority (aka pypa) have [assembled a user guide](http://python-packaging-user-guide.readthedocs.org/en/latest/index.html) for fellow travelers on the road to packaging nirvana. Unfortunately, it is very much a work in progress and a little thin on details in my opinion.

As a result, we'll mostly be mimicking the pypa's sample project, [found on their github](https://github.com/pypa/sampleproject). Let's compare our current project's structure against that.

rss2sms:

```
- .gitignore
- README.md
- rss2sms.py
```

pypa's sample project:

```
- sample/
- tests/
- .gitignore
- README.md
- DESCRIPTION.rst
- MANIFEST.in
- setup.py
- setup.cfg
```

Well...looks like we need some changes. Let's walk through a couple of these and explain what they're doing.

The most noticeable feature of a python package is the package directory. It will hold all the code necessary to run our package once it's installed. Let's start there and simply move our main module inside a directory named after the project. And just for fun, let's make a stub test directory that we can fill in properly later on.

```
 ~/Desktop/github/rss2sms (master) $ st
On branch master
Your branch is up-to-date with 'origin/master'.

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	renamed:    rss2sms.py -> rss2sms/__init__.py
	new file:   tests/__init__.py
```

Perfect. Now comparing to the sample package, the only remaining requirement is a `setup.py` module to tell python the basic details about our package.

## setup.py

As you may be aware, the history of python packaging is not particularly simple or straightforward. There are many [blog posts](http://blog.startifact.com/posts/older/a-history-of-python-packaging.html), good [talks at pycon](http://pyvideo.org/video/1601/twisted-history-of-python-packaging), and a variety of other sources to learn about the details. Some day I may even take a shot at a summary here. But for now, we're going to bypass all the history and jump straight to building a current `setup.py` for our package.

That said, let's take the [basic setup.py](https://github.com/pypa/sampleproject/blob/master/setup.py) and mold it to our purposes. I've inlined our basic version below:

``` python
from setuptools import setup, find_packages                                     
import codecs                                                                   
import os                                                                       
import re                                                                          
                                                                                   
                                                                                
def find_version(*file_paths):                                                  
    # Open in Latin-1 so that we avoid encoding errors.                         
    # Use codecs.open for Python 2 compatibility                                
    here = os.path.abspath(os.path.dirname(__file__))                           
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:      
        version_file = f.read()                                                 
                                                                                
    # The version line must have the form                                          
    # __version__ = 'ver'                                                       
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",            
                              version_file, re.M)                               
    if version_match:                                                           
        return version_match.group(1)                                           
    raise RuntimeError("Unable to find version string.")                        
                                                                                
                                                                                
# Get the long description from the relevant file                               
with codecs.open('DESCRIPTION.rst', encoding='utf-8') as f:                     
    long_description = f.read()                                                 

setup(                                                                          
    name="rss2sms",                                                             
    version=find_version('rss2sms', '__init__.py'),                             
    description="An sms alerter for updates to an rss feed",                    
    long_description=long_description,                                          
    url='http://github.com/striglia/rss2sms',                                   
    author='Scott Triglia',                                                     
    author_email='scott.triglia@gmail.com',                                     
    license='MIT',                                    
                                                                                
    classifiers=[                                                               
        'Development Status :: 3 - Alpha',                                      
        'License :: OSI Approved :: MIT License',                               
                                                                                
        'Programming Language :: Python :: 2',                                  
        'Programming Language :: Python :: 2.6',                                
        'Programming Language :: Python :: 2.7',                                
    ],                                                                          
    keywords='rss sms alerts',                                                  
                                                                                
    packages=find_packages(exclude=["tests*"]),                                 
    install_requires=[                                                          
        'feedparser',                                                           
        'tinyurl',                                                              
        'twilio',                                                               
    ],                                                                          
    entry_points={                                                              
        'console_scripts': [                                                    
            'rss2sms=rss2sms:main',                                             
        ],                                                                      
    },                                                                          
)                                          
```

Before we move on, let's make a brief note of the `install_requires` directive.

```
install_requires=[                                                          
        'feedparser',                                                           
        'tinyurl',                                                              
        'twilio',                                                               
    ],
```

This is where our package can specify all the other python packages it depends on to work. In my original script, I just blindly imported things and assumed they were available. In this new way, we can specify what we need and python will automatically install them when we install our package.


## One last thing

And final feature I'd like to add, even though it's not in the sample package, is a Makefile. You might be wondering why we need a Makefile at all here. Truth is, we don't really need one. The project is not that complicated and we don't need to actually build any dependencies to run the code.

That said, I like Makefiles as a generic interface to standard tasks for the package. In our case, I'd like there to be simple, implementation-agnostic commands to clean the project up and to run our tests.

This is pretty cheap to do with a Makefile. In fact, we can add this simple Makefile to do what I just described:

```
~/Desktop/github/rss2sms (master) $ cat Makefile 
clean:
	find ./ -name "*.pyc" -delete
test:
	py.test tests
```

Nothing complicated here yet, but it gives us the room to expand later on. Note that I am using the excellent [py.test package](http://pytest.org/latest/) to do my testing. I'm sure I'll talk more about how much I like it later, but you should definitely check it out in the meantime.

## Wrapping Up

With that, we're basically set. We have the core package structure down, and we can try to install our package locally. Let's test it out:

```
~/Desktop/github/rss2sms (master) $ virtualenv venv
New python executable in venv/bin/python
Installing Setuptools..............................................................................................................................................................................................................................done.
Installing Pip.....................................................................................................................................................................................................................................................................................................................................done.

 ~/Desktop/github/rss2sms (master) $ source venv/bin/activate

 (venv) ~/Desktop/github/rss2sms (master) $ python setup.py develop
 running develop
running egg_info
writing requirements to rss2sms.egg-info/requires.txt
writing rss2sms.egg-info/PKG-INFO
writing top-level names to rss2sms.egg-info/top_level.txt
writing dependency_links to rss2sms.egg-info/dependency_links.txt
writing entry points to rss2sms.egg-info/entry_points.txt
reading manifest file 'rss2sms.egg-info/SOURCES.txt'
writing manifest file 'rss2sms.egg-info/SOURCES.txt'
running build_ext
Creating /Users/striglia/Desktop/github/rss2sms/venv/lib/python2.7/site-packages/rss2sms.egg-link (link to .)
Adding rss2sms 0.0.1 to easy-install.pth file
Installing rss2sms script to /Users/striglia/Desktop/github/rss2sms/venv/bin

<many more lines of text here>

Installed /Users/striglia/Desktop/github/rss2sms/venv/lib/python2.7/site-packages/httplib2-0.8-py2.7.egg
Finished processing dependencies for rss2sms==0.0.1
```

Success! We have a package we can install locally, which knows about its dependencies (courtesy of setup.py) and which has very rudimentary testing and documentation. In future iterations of this series, I hope to jump into a lot of interesting topics - particularly better testing setups, simple invocations of our script from the command line, and even uploading to pypi. Until then, you can find all the code described [here on my github](https://github.com/striglia/rss2sms/tree/v0.0.1), under the tagged version 0.0.1 of rss2sms.
