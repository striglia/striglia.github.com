---
layout: post
title: "Elegant n-gram generation in Python"
date: 2013-01-20 12:51
comments: true
Category: python
---

A quick few snippets of code today -- solving how to compactly and elegantly generate n-grams from your favorite iterable.

<!-- more -->

For starters, let's talk about generating all bigrams from a python list (or anything we can iterate over). We'll write it generally so it can work over lists, strings, or whatever else you care to make iterable. Finally, I'll show the more general extension at the end.

## The obvious way

So our first shot here can be done with a single walk through our list:

``` python
input_list = ['all', 'this', 'happened', 'more', 'or', 'less']

def find_bigrams(input_list):
	bigram_list = []
	for i in range(len(input_list)-1):
		bigram_list.append((input_list[i], input_list[i+1]))
	return bigram_list
```

You could easily suggest that this for loop may be better written with zip() instead of just range(), but the basic idea would be the same -- iterate over each element and manually combine it with the one directly following it.

One thing I will mention here is that I'm not counting the first or last terms in their own bigrams (i.e. there is no bigram created that ends with 'all' or starts with 'less'). There are variations we could create that would include such bigrams (usually using some sort of padding value for the missing terms) but I will ignore them for the remainder of this discussion.

So we have the minimal python code to create the bigrams, but it feels very low-level for python…more like a loop written in C++ than in python. Let's change that.

## Slicing and Zipping

Let's take advantage of python's [zip builtin](http://docs.python.org/2/library/functions.html#zip) to build our bigrams. Zip takes a list of iterables and constructs a new list of tuples where the first list contains the first elements of the inputs, the second list contains the second elements of the inputs, and so on. Given this fact, it will construct our bigrams for us if we can just pass it two lists that contain the first and second elements of each bigram.

In fact, a little thought shows us that we can do this by simply passing in our original `input_list` once normally and once offset by one element. This gives us our second version of `find_bigrams`.

``` python
input_list = ['all', 'this', 'happened', 'more', 'or', 'less']

def find_bigrams(input_list):
	return zip(input_list, input_list[1:])
```

Hey now that is something you can show off around the office!

## Generalizing

Okay but seriously, let's not get too excited. We still need to pass in a bunch of arguments to zip(), arguments which will have to change if we want to do anything but generate bigrams. So let's fix that. What if we want to generate n-grams from a list and we wish to cleanly do that in a general way?

If we write out what our zip() invocation looks like for various n-grams, we see a pattern:

``` python
# Bigrams
zip(input_list, input_list[1:])
# Trigrams
zip(input_list, input_list[1:], input_list[2:])
# and so on
zip(input_list, input_list[1:], input_list[2:], input_list[3:])
```

Notice the pattern? If we could construct those arguments programmatically, just given the N we want to generate n-grams for, we'd be all set! So let's do that. We're going to leverage two things -- list comprehensions and the `*` operator to build up our arguments.

We can easily write a list comprehension to build up the list of inputs - `[input_list[i:] for i in range(n)]`. After we've done this, we need to take a list of arguments and unlist them. This is the exact purpose of the underused `*` operator in python. It is perfect for our purpose, taking a list and passing all elements into a function call.

And now we have all our ingredients organized for our general find_ngram method.

``` python
input_list = ['all', 'this', 'happened', 'more', 'or', 'less']

def find_ngrams(input_list, n):
	return zip(*[input_list[i:] for i in range(n)])
```

And there you go! It is worth noting that this is probably a suggestion too clever for it's own good…but it's also a great opportunity to practice the application of list comprehensions and the itertools module. Happy hacking!
