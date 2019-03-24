---
layout: post
title: "There is no such thing as magic"
date: 2014-03-11 22:43
comments: true
Category: python
---

Do you know my favorite fact about programming? In the end, everything is build from code and you can understand it all -- there is absolutely no magic. With enough effort, almost everything you interact with can be dug into, demystified, and explained. I know I often interact with various tools I use as if they were black boxes, either for lack of time, lack of interest, or a fear that I wouldn't understand them if I tried. But let's fight back against that.

So for this post, let's understand what's going on with python's [virtualenv package](http://www.virtualenv.org/).

<!-- more -->

## The Basics

Let's start out simple -- the purpose and use of virtualenv. Stealing directly from the project's homepage, "virtualenv is a tool to create isolated Python environments." Well great...what good is that?

### A little backstory

I'll explain by virtue of a story about my travails with scipy. If you don't know, installing scipy/numpy on OS X has historically been...challenging. Numerous system-level dependencies, old versions of numpy pre-installed on the machine both complicate what is already a non-trivial installation procedure. This leads to a ton of posts like [this](http://stackoverflow.com/questions/11517164/scipy-numpy-matplotlib-troubles-on-osx) or [this](http://penandpants.com/2012/02/24/install-python/) and even extensive [step-by-step guides](http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/). Although scipy suffers from some complications surrounding required non-python bits (like fortran compilers), the most frequent problem I've had installing is simply having conflicting versions of numpy installed.

That brings us to Virtualenv, and its use case. Macs come helpfully pre-installed with an old and unhelpful version of numpy.

``` bash
$ python -c 'import numpy; print numpy; print numpy.__version__'
<module 'numpy' from '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/__init__.pyc'>
1.5.1
```

Well that won't work well with my hope to use the (very cool) data analysis library `pandas`. In fact, the [pandas installation page](http://pandas.pydata.org/pandas-docs/stable/install.html) kindly points out that it requires numpy 1.6.1 or higher! How can we install pandas without changing the system installed version of numpy? Enter virtualenv.

### Our very first virtualenv

I promised I'd start out with a quick example, so let's show how virtualenv solves our little scipy snafu in a pinch.

Virtualenvs are their own little world -- by default they are entirely isolated from your system installed python packages. First lets install virtualenv (the last thing we'll need to install globally!) and set up a sample env.

``` bash
 ~  $ sudo pip install virtualenv
Downloading/unpacking virtualenv
  Running setup.py egg_info for package virtualenv
    
    warning: no files found matching '*.egg' under directory 'virtualenv_support'
    warning: no previously-included files matching '*' found under directory 'docs/_templates'
    warning: no previously-included files matching '*' found under directory 'docs/_build'
Installing collected packages: virtualenv
  Running setup.py install for virtualenv
    
    warning: no files found matching '*.egg' under directory 'virtualenv_support'
    warning: no previously-included files matching '*' found under directory 'docs/_templates'
    warning: no previously-included files matching '*' found under directory 'docs/_build'
    Installing virtualenv script to /usr/local/bin
    Installing virtualenv-2.7 script to /usr/local/bin
Successfully installed virtualenv
Cleaning up...
~  $ virtualenv my_first_env
New python executable in my_first_env/bin/python
Installing Setuptools..............................................................................................................................................................................................................................done.
Installing Pip.....................................................................................................................................................................................................................................................................................................................................done.
~  $ source my_first_env/bin/activate
(my_first_env) ~  $ echo 'hello world'
hello world
```

Excellent! We installed virtualenv on our system using pip, created a virtualenv called `my_first_env`, and finally activated it. This means that python is now entirely isolated from system packages. Let's prove it to ourselves by trying to import some packages we know are installed on this machine.

``` bash
(my_first_env) ~  $ python -c 'import pytz; print pytz'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named pytz
(my_first_env) ~  $ python -c 'import numpy; print numpy'
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named numpy
```

And we can also test the same commands outside our virtualenv to confirm they work!

``` bash
(my_first_env) ~  $ deactivate
 ~  $ python -c 'import pytz; print pytz'
<module 'pytz' from '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/pytz/__init__.pyc'>
 ~  $ source my_first_env/bin/activate
```

Interesting. And how about installing that fresh new package we had our eyes on?

``` bash
(my_first_env) ~  $ pip install pandas
Downloading/unpacking pandas
  Downloading pandas-0.12.0.tar.gz (3.2MB): 3.2MB downloaded

-----(it continues for a while installing various dependencies)-----

Successfully installed pandas python-dateutil pytz six
Cleaning up...
```

And there we go! We can now happily play around with all of the installed packages inside of our virtual environment and we did it without affecting any other users of this computer, or requiring global install privileges.

## Well that was magical

If you're anything like me, your natural first reaction to a new tool like this is to feel a little uncomfortable. You can go through the motions (perhaps copying from some tutorial you found on a blog) and hope things will still work, but there's no real understanding of how this new tools works. Maybe you even resign yourself to never understanding something and just keep using it the way you were taught, effectively becoming a [cargo cult programmer](http://en.wikipedia.org/wiki/Cargo_cult_programming).

Avoiding that behavior is exactly the point of this blogpost, and I think it's perhaps **the** most powerful skill for any programmer. Digging into an unfamiliar project and building a mental model of how it works is the essence of programming! If you truly understand how something is put together, you can modify it, improve it, or explain it with ease.

So for the rest of this post, let's dig in and prove virtualenv isn't magic. We will both be taking this journey together, as I've never dug into its guts either. So let's see what we can figure out.

## Going to the source

So lets crack open `virtualenv` and understand what's actually happening.

There are three main scripts we keep calling to create, activate, and deactivate a virtualenv -- `virtualenv`, `venv/bin/activate` and `deactivate`. Let's deal with creating the environment with `virtualenv` before jumping into activation/deactivation.

### Creating a virtualenv

Opening up the file at `which virtualenv` drops me into the source:

``` python
#!/usr/bin/python                                                               
# EASY-INSTALL-ENTRY-SCRIPT: 'virtualenv==1.10.1','console_scripts','virtualenv'
__requires__ = 'virtualenv==1.10.1'                                             
import sys                                                                      
from pkg_resources import load_entry_point                                      
                                                                                
sys.exit(                                                                       
   load_entry_point('virtualenv==1.10.1', 'console_scripts', 'virtualenv')()       
)  
```

Well that's not very helpful. Looks like running `virtualenv` is actually just executing this bit of code. Time to see if we can figure out what `load_entry_point` is and what it is actually calling.

A little googling later, we find [this SO post](http://stackoverflow.com/a/9615473) on the subject. Looks like in nice python packages, entry points are defined in `setup.py` and automatically linked to runnable scripts at installation time. We can download the source from [pypi](https://pypi.python.org/pypi/virtualenv) and take a look ourselves.

Sure enough, when we open up `setup.py` we see the entry_point dict we were promised:
``` python
setup_params = {                                                            
    'entry_points': {                                                       
        'console_scripts': [                                                
            'virtualenv=virtualenv:main',                                   
            'virtualenv-%s.%s=virtualenv:main' % sys.version_info[:2]          
        ],                                                                  
    },                                                                      
    'zip_safe': False,                                                      
    'test_suite': 'nose.collector',                                         
    'tests_require': ['nose', 'Mock'],                                      
}
```

Indeed they seem to be linking the runnable `virtualenv` python script to the `main` function of virtualenv.py. Let's see what that looks like. The content of the main function appears to roughly follow these steps:

- Build an option parser with `optparse`
- Check if the script was called with the `--python` interpreter option and possibly exit.
- Take actions based on various command line options
- Call the `create_environment` method!

Well now that last one sounds quite relevant! Here's the full text of the create_environment method:

``` python
def create_environment(home_dir, site_packages=False, clear=False,                                   
                       unzip_setuptools=False,                                                       
                       prompt=None, search_dirs=None, never_download=False,                          
                       no_setuptools=False, no_pip=False, symlink=True):                             
    """                                                                                              
    Creates a new environment in ``home_dir``.                                                       
                                                                                                     
    If ``site_packages`` is true, then the global ``site-packages/``                                 
    directory will be on the path.                                                                   
                                                                                                     
    If ``clear`` is true (default False) then the environment will                                   
    first be cleared.                                                                                
    """                                                                                              
    home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)                                   
                                                                                                     
    py_executable = os.path.abspath(install_python(                                                  
        home_dir, lib_dir, inc_dir, bin_dir,                                                         
        site_packages=site_packages, clear=clear, symlink=symlink))                                  
                                                                                                     
    install_distutils(home_dir)                                                                      
                                                                                                     
    if not no_setuptools:                                                                            
        install_sdist('Setuptools', 'setuptools-*.tar.gz', py_executable, search_dirs)               
        if not no_pip:                                                                               
            install_sdist('Pip', 'pip-*.tar.gz', py_executable, search_dirs)                         
                                                                                                     
    install_activate(home_dir, bin_dir, prompt)
```

Now we're getting somewhere! It looks like the basic steps are:

1. Get a bunch of path locations based on the `home_dir` path
2. Install python inside our environment and return a path to the executable
3. Install some subset of `distutils`, `setuptools` and `pip`
4. Install the `activate` scripts into this new virtualenv

And that's the essence of what running `virtualenv` does: it defines paths for the interpreter, libraries and binaries; installs the interpreter and installation-related python packages; and it installs the `activate` script so you can activate it. And we now understand what goes into creating a new virtualenv.

### Activating and Deactivating

So that leaves the question of what `activate` and `deactivate` are up to. We can inspect the activate script easily enough by running `vim my_first_env/bin/activate`.

The first thing we notice is that a bash function `deactivate` is defined immediately. We'll get back to this later in this section, but this is actually the definition of the `deactivate` method we call to leave the virtualenv. The relevant lines are so brief, you might miss them entirely:

``` bash
_OLD_VIRTUAL_PATH="$PATH"                                                       
PATH="$VIRTUAL_ENV/bin:$PATH"                                                   
export PATH
```

Note that we're saving the old `PATH` and making a new one, with our local virtualenv prepended! This means that the next time we run `python`, we'll get the interpreter we installed into our virtualenv, which is pointed at all our own libraries instead of the default system-installed interpreter. With that in mind, let's look at the `deactivate` function.

``` bash
deactivate () {                                                                 
    unset pydoc                                                                 
                                                                                
    # reset old environment variables                                           
    if [ -n "$_OLD_VIRTUAL_PATH" ] ; then                                       
        PATH="$_OLD_VIRTUAL_PATH"                                               
        export PATH                                                             
        unset _OLD_VIRTUAL_PATH                                                 
    fi                                                                          
    if [ -n "$_OLD_VIRTUAL_PYTHONHOME" ] ; then                                 
        PYTHONHOME="$_OLD_VIRTUAL_PYTHONHOME"                                   
        export PYTHONHOME                                                       
        unset _OLD_VIRTUAL_PYTHONHOME                                           
    fi                                                                          
                                                                                
    # This should detect bash and zsh, which have a hash command that must      
    # be called to get it to forget past commands.  Without forgetting          
    # past commands the $PATH changes we made may not be respected              
    if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then                               
        hash -r 2>/dev/null                                                     
    fi                                                                          
                                                                                
    if [ -n "$_OLD_VIRTUAL_PS1" ] ; then                                        
        PS1="$_OLD_VIRTUAL_PS1"                                                 
        export PS1                                                              
        unset _OLD_VIRTUAL_PS1                                                  
    fi                                                                          
                                                                                
    unset VIRTUAL_ENV                                                           
    if [ ! "$1" = "nondestructive" ] ; then                                     
    # Self destruct!                                                            
        unset -f deactivate                                                     
    fi                                                                          
}
```

The important part here is the resetting of old environment variables (notably `PATH`).

You can notice other details in this file, like the setting/unsetting of your [shell prompt](http://www.cyberciti.biz/tips/howto-linux-unix-bash-shell-setup-prompt.html) to include the name of the currently active virtualenv.

And that's it -- you've uncovered the basics of how virtualenv works!

## Just the beginning

Just like that, we've taken a nontrivial tool and pulled it apart into understandable pieces. I certainly didn't understand every part of what we found immediately (and that's perfectly okay and expected!), but through some persistent searching and effort, it all makes sense. And every time I go through this process with a new tool, I find myself understanding more and more of what is going on, and gaining greater familiarity with various python tools.

On the subject of virtualenv in particular, I've since discovered [this excellent overview of the its guts](http://blip.tv/pycon-us-videos-2009-2010-2011/pycon-2011-reverse-engineering-ian-bicking-s-brain-inside-pip-and-virtualenv-4899496) from PyCon 2011. Take a look if you're interested in even more detail on the subject (like why does using a particular python interpreter change where I look up system packages).

So go find something you don't understand! I've been elbow deep in learning the various horrors of python packaging lately, so perhaps I'll continue this series with a look into some aspect of that. Either way, I hope I've encouraged you to not be afraid of jumping into unfamiliar territory and transforming code from mysterious to understood.
