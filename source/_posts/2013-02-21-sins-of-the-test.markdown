---
layout: post
title: "Sins of the Test"
date: 2013-02-21 22:27
comments: true
categories: testing
---

We all make mistakes…some more embarrassing than others in hindsight. I always really appreciate when programmers I look up to make a point of pointing out their own faults, so I figured it was only fair for me to do the same.

So in that spirit, let's talk about where I've gone wrong! Looking back on the tests I've written in the last six months has made me realize several things I'd change if I could write them again.

<!-- more -->

## abusing subclasses

First up -- the misuse of classes and inheritance.

A mere six months ago, I wrote something approximating the following series of tests for a new feature I was rolling out:

``` python
from experiment_framework import configure_experiment
from our_logic_module import method_under_test

class TestSecretFeatureBase(TestCase):
	__test__ = False  # Make sure this class is purely abstract
	activate_feature = None
	necessary_input = None
	expected_output = None
	
	def test_class_vars_are_set(self):
		"""Enforce class variables being set in the subclass"""
		assert self.activate_feature is not None
		assert self.necessary_input is not None
		assert self.expected_output is not None
	
	def test_output_of_method(self):
		"""The test we actually care about"""
		configure_experiment('my_secret_feature', self.activate_feature)
		
		output = method_under_test(self.necessary_input)
		assert output == expected_output

class TestSecretFeatureOff(TestCase):
	# Test what happens when we turn our feature off!
	activate_feature = False
	necessary_input = 'some required arg'
	expected_output = 'magic'

class TestSecretFeatureOn(TestCase):
	# Test what happens when we turn our feature on!
	activate_feature = True
	necessary_input = 'some required arg'
	expected_output = 'more magic'

```

Let's briefly cover what this was designed to do. We have a method `method_under_test` that we want to run with some necessary arguments, testing each time that the output is what we expect. In particular, we want to test this method with a new secret feature turned both on and off.

So what's bad about this? The big lesson I learned from looking back on this was that I had painfully abused the concept of a test suite in an attempt to be DRY. Note that the above solution has no single test suite that can be called -- in fact each test is segregated into its own test suite! Nasty! And the only reason I did all this was to create a few real test cases (the classes TestSecretFeatureOn/TestSecretFeatureOff here) with a bunch of variables that are required to be defined.

Instead, I should have written the entire base class as a simple function with just `necessary_input` and `activate_feature` as arguments. The tests themselves could then be grouped into a single meaningful (and useful!) test suite and the `test_class_vars_are_set` eliminated entirely since it would be implicitly required by the function signature. 

Check out the improved code:
``` python
def run_method_under_test_with_experiment(activate_feature, necessary_input):
	"""Runs method_under_test with our secret experiment set according to the
	passed flag and returns the result.
	"""
	configure_experiment('my_secret_feature', activate_feature)
	return method_under_test(necessary_input)

class TestSecretFeature(TestCase):
	"""Test suite covering the soon-to-be-released Secret Feature"""
	necessary_input = 'some required arg'
	
	def test_feature_off(self):
		assert run_method_under_test_with_experiment(False, self.necessary_input) == 'magic'
		
	def test_feature_on(self):
		assert (run_method_under_test_with_experiment(True, self.necessary_input) == 'more magic'
```

Just like that, we have collapsed all our tests into a single descriptive test suite and we can reliably know that classes always contain meaningful collections of tests. Maybe most importantly, it's much simpler for the next poor dev who has to unravel the goal of my tests.

## test method names

Next up, needlessly abbreviating test method/suite names!

In non-test code, there are some plausible arguments that long method names are cumbersome -- you will often call them multiple places and some additional brevity can be worthwhile. In my experience with tests however, something like 95% of the test methods or test suites I name will *never be typed again* outside the method/class definition. This means long names not only don't cost me anything, they're essentially a free chance to eliminate docstrings that may be otherwise unnecessary.

Not too much else to say here, just consider the following before and after from some only-slightly-sanitized production code of mine:

``` python
class FilteringTest(TestCase):
	"""Tests that low scoring candidates are removed by filtering."""
	
	def test_return_few_candidates(self):
	"""Test _filter_candidates correctly prunes results, below the request's threshold."""
```

Instead, let's just express those docstrings directly in the names. Easier to read, easier to debug if you only see failing test names, everyone wins!

``` python
class FilterCandidatesTest(TestCase):
	
	def test_candidates_below_score_threshold_are_not_returned(self):
```

## too few test suites

A simple one, but something that's been on my mind. If we're using test classes 90% of the time for just organization purposes, then what use is it to clump together a large number of tests in a single suite? If I'm trying to tweak a particular feature, but have to choose between running either a single unit test or far too many of them, I'm probably not going to be doing small, iterative changes with lots of testing because it'll just be too slow.

Instead, break into a new class per distinct functionality. If you're awesome, this probably looks suspiciously close to one class per method under test, and a relatively small number of classes per object under test. If you're like me and still working toward that goal, you can still aim for making small, focused suites so that changes to code will break relatively few suites, and a single suite can be quickly re-run. Admittedly, this type of organization does depend on the particular choices of your chosen testing framework and its mechanism for determining what a suite is.

## not listening to what tests are telling me

If I had to sum up the most important thing I'd learned in the last year from testing it's this point -- if it's hard to test something (class, function, whatever), you should assume there is room (maybe a lot of it) for improving it. This almost seems pointless to say, except that I cannot tell you how many times I've spent a day bumbling my way through writing/modifying just a couple tests on an old, crufty object without bothering any refactoring of the thing under test.

To rephrase, if something sucks to test, assume guilt until innocence is proven. It's almost never a bad exercise to look at your code with a critical eye toward untangling mixed responsibilities, ugly dependences, or sheer bloat. Worst case scenario, you don't see anything that can be fixed and you soldier on. But more likely, you will see something you can tweak to make both future coding and testing easier. Win win.

Know what rarely is a pain to test? The best code I've written. In fact, it's also often the best tested. Curious…

## always improving

Well that's enough of my rambling, but I hope this gives you a few ideas for attacking your own tests. If nothing else, it is an excellent exercise to step back from the daily grind and trying to look for longer-term patterns you see. It's far too easy to get stuck in local optima because they're familiar, even if you yourself have experienced better! Here's to always improving.
