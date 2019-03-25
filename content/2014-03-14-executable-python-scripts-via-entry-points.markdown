---
layout: post
title: "Executable python scripts via entry points"
date: 2014-03-14 16:11
comments: true
Category: python
---

A quick topic -- executing a python module from the command line!

<!-- more -->

When [I last left](http://locallyoptimal.com/blog/2014/03/14/building-a-basic-package-pt-1-bare-bones/) my pet rss2sms project, it had been transformed into a basic python package. Unfortunately, this means that my old method of running `python rss2sms.py --foobar` from the command line is not so simple anymore. In fact what I really want is to be able to just run `rss2sms --foobar` from the command line after I install the package.

Luckily python has exactly what we need in the form of setuptools's [console_script argument to entry_points](http://pythonhosted.org//setuptools/setuptools.html#automatic-script-creation).

Let's go ahead and add it to our setup.py:

``` python
setup(
	name="rss2sms",                                                             
    version=find_version('rss2sms', '__init__.py'),                             

# ...the rest of our setup.py here....

	entry_points={                                                              
        'console_scripts': [                                                    
            'rss2sms=rss2sms:main',                                             
        ],                                                                      
    },
)
```

So simple! Note that we're linking the executable `rss2sms` here to running the python function `main` in the `rss2sms` module. If we look at that function, it just does the normal command line parsing and function calling that it always has.

``` python
def main():                                                                     
    parser = OptionParser()                                                     
    parser.add_option("-u", "--url", dest="rss_url",                            
                            help="url of rss feed")                             
    parser.add_option("-t", "--to", dest="to_num",                              
                            help="cell number to send sms alerts to")           
    parser.add_option("-f", "--from", dest="from_num",                          
                            help="cell number to send sms alerts to (overrides environment variable TWILIO_NUMBER)")
    parser.add_option("-i", "--id", dest="rss_id_field",                        
                            help="unique id rss field used for display in SMS and for equality comparison (defaults to 'link')")
    parser.add_option("-d", "--display", dest="rss_display_field",              
                            help="name of rss field used for display in SMS (defaults to 'title')")
    parser.add_option("-c", "--cache-filename", dest="cache_filename",          
                            help="optional file to cache last post in")         
                                                                                
    (options, args) = parser.parse_args()                                       
    rss2sms = Rss2Sms(**vars(options))                                          
    rss2sms.parse_and_alert() 
```

Now let's start up a fresh virtualenv and test it out. We can use pip's develop option to install a package by just passing it a path.

```
~/Desktop/github/rss2sms (master) $ virtualenv entry_point_test; source entry_point_test/bin/activate
New python executable in entry_point_test/bin/python
Installing Setuptools...........done.
Installing Pip..................done.
(entry_point_test) ~/Desktop/github/rss2sms (master) $ pip install -e .

... lots of text from installation...

(entry_point_test) ~/Desktop/github/rss2sms (master) $ rss2sms --help
Usage: rss2sms [options]

Options:
  -h, --help            show this help message and exit
  -u RSS_URL, --url=RSS_URL
                        url of rss feed
  -t TO_NUM, --to=TO_NUM
                        cell number to send sms alerts to
  -f FROM_NUM, --from=FROM_NUM
                        cell number to send sms alerts to (overrides
                        environment variable TWILIO_NUMBER)
  -i RSS_ID_FIELD, --id=RSS_ID_FIELD
                        unique id rss field used for display in SMS and for
                        equality comparison (defaults to 'link')
  -d RSS_DISPLAY_FIELD, --display=RSS_DISPLAY_FIELD
                        name of rss field used for display in SMS (defaults to
                        'title')
  -c CACHE_FILENAME, --cache-filename=CACHE_FILENAME
                        optional file to cache last post in
```

And just like that we have an executable hooked up our python module. We can even use which to see how it works:

```
(entry_point_test) ~/Desktop/github/rss2sms (master) $ which rss2sms
/Users/striglia/Desktop/github/rss2sms/entry_point_test/bin/rss2sms
(entry_point_test) ~/Desktop/github/rss2sms (master) $ cat `which rss2sms`
#!/Users/striglia/Desktop/github/rss2sms/entry_point_test/bin/python            
# EASY-INSTALL-ENTRY-SCRIPT: 'rss2sms==0.0.1','console_scripts','rss2sms'          
__requires__ = 'rss2sms==0.0.1'                                                 
import sys                                                                      
from pkg_resources import load_entry_point                                      
                                                                                
if __name__ == '__main__':                                                      
    sys.exit(                                                                   
        load_entry_point('rss2sms==0.0.1', 'console_scripts', 'rss2sms')()         
    )  
```

This executable is just a simple python module which, when we call it, uses the pkg_resources library to look up what python module our setup.py says we should call. All in all, a very painless way to distribute nice executables for your library.
