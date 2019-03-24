---
layout: post
title: "Why namedtuples?"
date: 2012-09-08 22:36
comments: true
Category: python
---

If you had asked me to explain all I knew about Python's namedtuple class at
the start of this year, I would have probably muttered something about
mutability and trailed off into an uncomfortable silence. The fact of the
matter was, I had seen them used once or twice but never really understood the
reason they were used. Hopefully by the end of this entry I can explain at
least a couple of places you might consider using them over the typical Python
class.

<!-- more -->

One of my favorite ways to be introduced to any new concept is by seeing the
simplest example that still motivates its use. In the case of namedtuples, I'm
partial to the example below, which compares two proposed implementations of
a latitude/longitude coordinate -- something I get a lot of experience with in
my day to day work life -- and does some basic manipulation of their contents.

``` python
# The primitive approach
lat_lng = (37.78, -122.40)
print 'The latitude is %f' % lat_lng[0]
print 'The longitude is %f' % lat_lng[1]

# The glorious namedtuple
LatLng = namedtuple('LatLng', ['latitude', 'longitude'])
lat_lng = LatLng(37.78, -122.40)
print 'The latitude is %f' % lat_lng.latitude
print 'The longitude is %f' % lat_lng.longitude
```

By itself, this example is a little forced, but you can already see some benefits:

* increased readability of the print statements instead of cryptic indexing
* the presence of a LatLng class that gives a clear specification (instead of the next person who comes along representing it as a dictionary with two keys, or two floats, and so on...)

So you may well be asking yourself...why not just make a LatLng class?

An obvious question indeed. If we just stopped at the first example, you could
make a strong argument that a normal Python LatLng class with two attributes
would do everything we wanted without all this fuss. This brings us to the most
important difference between namedtuples and normal Python classes --
attributes in namedtuple subclasses are immutable once created, much like the
tuples for which the class is named. 

``` 
>>> LatLng = namedtuple('LatLng', ['latitude', 'longitude'])
>>> lat_lng = LatLng(37.78, -122.40) 
>>> lat_lng.latitude = 9.23
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
```

### Why do I care about mutability? ###

If you're anything like me, you're probably quite used to the idea of writing
highly stateful programs. Maybe you aren't even sure why some immutable class
is the subject of this entire blog entry...all the good stuff gets done by the
smart mutation of objects anyway, right? Well let me try to convince you of the
merits of immutability with a couple examples, hard-won lessons I've taught
myself several times over.

Anyone who has spent more than a couple weeks programming Python has probably
been bitten by accidentally modifying a data structure they thought was fixed:

```python
def totally_innocent_function(movie_list):
    movie_list.append('You Got Served')

the_best_movies_of_all_time = ['The Godfather', 'Citizen Kane', '2001: A Space Odyssey']
totally_innocent_function(the_best_movies_of_all_time)
```

Just because you think your data structure is properly structured and validated
doesn't prevent a well intentioned person from later modifying it, possibly
even in a way where you don't ever realize it happened. If you are lucky, this
gets noticed and fixed immediately. If you're unlucky, the bug silently
festers, doing who-knows-what to your application. In my experience, the
original author and the well intentioned person who breaks the code later on
are typically both myself. Coding is complicated and allowing your data to be
mutable when you don't want it to be can lead to trouble.

### And what if I need more than simple attributes? ###

In most of my personal uses of namedtuples, I inevitably have some additional functionality I wanted from the class -- often some computed result of the various attributes built into the class. Sounds an awful lot like a property right? Give something like the following a shot. You get all the benefits of knowing your core data isn't going to be accidentally modified while also getting fancy properties on the side!

{% include_code namedtuple_properties.py %}
``` python
```

### Everything in moderation ###

So I hope I've at least suggested to you the benefits of trying out
namedtuples, for both code readability and safety. It's certainly possible to
take this too far, but at the very least it's an excellent way to learn a new
approach and get to investigate some of Python's more niche features.
