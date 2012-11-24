---
layout: post
title: "Hiding complexity with Context Managers"
date: 2012-10-21 14:53
comments: true
categories: python
---

Very reliably, my favorite part of programming is the simple process of taking a series of steps that I used to have to do by hand and packaging it up in a nice, reusable form. It's pretty wonderful that it remains just as rewarding now as it did when I wrote my first function in C++ 8 years ago.

So in that spirit, I figured I'd write down a few thoughts on python's context managers -- the latest built-in feature that I've grown quite attached to. 

## The basics

Context managers are, at their most basic, blocks of code which do something when they are entered and exited. You can see the full description of them in the excellent [python docs page](http://docs.python.org/reference/datamodel.html#context-managers) or [PEP 343](http://www.python.org/dev/peps/pep-0343/). Suffice it to say, they execute code when their `with` block is entered and exited, allowing nice convenience methods to exist. An excellent (built in!) example is reading from a file while making sure to close it again at the end…in fact you likely have used this already once or twice.

Old and busted:

```
input_file = open('config.txt', 'r')
print input_file.read()
input_file.close()
```

Nice and convenient:

```
with open('config.txt', 'r) as input_file:
	print input_file.read()
```

Behind the scenes, the `with` statement is opening the file, binding the file object to the input_file variable, and then closing the file again after we exit the code block. Nothing complicated at all, but this provides a very nice tool for creating really pretty contexts that can do a lot of the heavy lifting behind the scenes.

## Writing our own

So that's the basic idea, but the natural next step is wanting to write one of your own! You can consult the python docs to learn how to set up your own context manager class, but I prefer leveraging a simpler approach where possible.

Our secret is going to be `contextlib`'s `contextmanager` decorator. Using it is as simple as decorating an appropriate function with `@contextmanager`. Let's write a toy example to show off the various parts of flow through a context manager.

{% codeblock lang:python %}
from contextlib import contextmanager

@contextmanager
def our_toy_context_manager(enter_msg, exit_msg):
	print enter_msg
	yield 'returned value!'
	print exit_msg

if __name__ == '__main__':
	with our_toy_context_manager('entering!', 'exiting!') as inner_msg:
		print inner_msg
{% endcodeblock %}

When run, this produces:

```
~/Desktop  $ python toy_context_manager.py 
entering!
returned value!
exiting!
```

Let's dive into how this decorator works. Keep in mind we can separate context managers into "before" and "after" blocks of code.

The first thing to notice is the `yield` statement in `our_toy_context_manager`. This yield marks the point where our context manager is done with the "before" portion of its code and returns an object to the calling code. In particular, when we write something like `with foo() as bar:`, the `bar` variable will refer to whatever is returned by this yield. In our example, the value returned is a string and it gets referred to by the `inner_msg` variable, and summarily printed.

After we are done executing the code inside our with context, we now return to `our_toy_context_manager` and execute the remaining code after the yield. And that's it! So while this example is quite contrived, you can see how easy it is to construct your own context managers that do something less trivial. In fact, let's try just that.

## The big leagues

In the spirit of my recent preoccupation with effectively testing larger systems, let's assume that we have a moderately complicated `Frobinator` object. Moreover, this object is used by a lot of other systems, and our corporate overlords have decreed that we must make a method available for easily mocking out calls to the `Frobinator.frobinate` method and specifying the return value.

You and I, being the knowledgeable stewards of the `Frobinator` that we are, know that there are significant complications involved in setting up a proper mock for testing, including limiting some logging that happens on every request and disabling some built in caching infrastructure. So we have our work cut out for us. Luckily, context managers nicely compliment the setup, assert, teardown format of mocks in tests. In our case, we need to set up a valid `Frobinator`, while simultaneously disabling caching and silencing logging. 

Our game plan is to construct a context manager called `mock_frobinator` which will have already disabled logging and caching, and will be a mock.Mock instance on the `frobinate` method so consumers can do any asserting they want on the testing side. Last but not least, we will set up our context manager to take a `results` variable as an argument and that will be set to be the return value of `Frobinator.frobinate` whenever it is called. So let's gather what we've learned so far and write this.

Or if you prefer, just look below =)

{% codeblock lang:python %}
from mock import Mock
from mock import patch
from contextlib import contextmanager

@contextmanager
def mock_frobinator(results):
	"""A mocked Frobinate object for convenient testing.
	
	Patches out both logging and caching to simplify execution.
	
	Yields a Mock for the frobinate method.
	
	Args:
		results - This will be set to always be the return value of calling Frobinator.frobinate.
	"""
	frobinator = Frobinator()
	mocked_frobinate = Mock(return_value=results)
	
	with patch.object(frobinator, 'frobinate', mocked_frobinate):
		with patch.object(frobinator, 'get_cached_results', Mock(return_value=None)):
				with patch.object(frobinator, 'write_to_log', Mock()):
					yield mocked_frobinate

if __name__ == '__main__':
	results = []
	with mock_frobinator(results) as mocked_frobinate:
		assert mocked_frobinate.call_count == 0
		res = mocked_frobinate()
		assert mocked_frobinate.call_count == 1
		assert res == results
{% endcodeblock %}

And just like that, we have a fairly complicated testing fixture hidden away from view, and a nice, convenient context manager exposed for others to use. And if we need to change what we're mocking out, or even disable a new part of the Frobinator, we can do it in a single place instead of every test which uses it.

## Final thoughts

Context managers are a great tool…not least of all because they provide a new metaphor (enter, do stuff, exit) for you to use where it makes the most sense. And after all that's the real benefit of diving into all these python standard library modules -- the more tricks you have up your sleeve, the better you can pick and choose the right tool for each job.