---
layout: post
title: "Testing with Mock"
date: 2012-09-10 19:34
comments: true
categories: 
---

More than any other area, I've found software testing to be the discipline which I knew the least about before joining up at Yelp full time. Sure, there was the normal insistence in my time as an undergraduate that I learn how to test units of code, and I'd heard plenty about the value of unit testing from any number of people or blogs, but when it came right down to it relatively few people I knew ever employed it to a meaningful degree during college and my graduate work. The simple truth was that projects rarely lasted long enough for the fruits of proper testing to be borne out.

Now I am sure plenty of people would disagree with that statement, pointing to how their various school projects were made better or simpler by judicious application of unit tests, but the goal of this post isn't arguing about whether or not testing is worthwhile. My goal is to dive in a little bit to one particular area of testing that I had essentially zero exposure to before joining industry -- the mocking of methods in tests.

<!-- more -->

### The basics of mocks ###

Given my complete ignorance the first time I was exposed to mocks, I'll start at the beginning -- a simple definition. Now there's some disagreement on the basic terms involved here, but I will default to [Martin Fowler's use of the work mock](http://martinfowler.com/articles/mocksArentStubs.html), and summarize it as follows.

To mock a method for a test involves verifying behavior. This can include:

1. asserting that it is called the expected number of times
1. asserting that it is called with the expected arguments
2. and finally replacing its normal execution with the execution of a stand-in method (or a fixed return value)

You'll immediately notice two distinct purposes to mocking in tests. First, they define (moreover, assert!) an interface between the code under test and the method you are mocking out. This is done both by agreeing upon the arguments passed to the mocked method and by checking how many times the method is called. Separate from these interface tests, the method itself is replaced by an imposter for the sake of this test.

So I've briefly described the spirit of a mock, but have left it entirely without motivation. Isn't the entire point of tests to actually test the real system? If I replace part of my code with something else, doesn't this mean any bugs in the mocked out code will be hidden from my tests? Strictly speaking, these complaints are valid. Mocking out a method means, for that test, the method's true code will not be exercised.

But prepare yourself for this, because it blew my mind the first several times I heard it -- that is the entire point.

### Why mock at all? ###

Outrage! Mutiny! What good is a test that doesn't actually test the code?! Well collect yourself, settle down, and I'll give you a real-world example that I hope will justify what I'm describing.

Let's imagine an extremely simple program, one almost too simple to test at all. Our goal is to write a tiny little wrapper around [Google's Geocoding API](https://developers.google.com/maps/documentation/geocoding/). In case you aren't already familiar with the concept of a geocoder, I'll summarize it very simply for our purposes as a black box that takes in a string, e.g. 'Mission District, San Francisco', and returns its best guesses at the location you are interested in, along with detailed information on each like longitude/latitude, city, state, country and so on.

So back to our program. Envision a simple application, which is meant to accept a city name and return you the list of American states which contain a city of that name. Our actual implementation will be a simple wrapper around Google's API where, if the original submitted city name was 'Foobar', we will search for 'Foobar, AL', 'Foobar, AK', and so on with each state name, recording when we get matches and returning the whole list at the end. Forgive me the clumsy example, but it will prove easy to reason about. 

Now lets think about testing our little utility....what parts of our program really need to be tested? Let's throw together a few likely prospects:

1. We should test to make sure we're constructing our places to geocode correctly.
2. Our validation of Google's responses should be tested (if Google has a match for 'Foobar, CA', and we were searching for 'Foobar' as our city, do we add California to our list of matched states?)
3. And just for kicks we may as well make sure the whole system runs properly

Cool...we've got our plan together. Let's assume we really want to test the
above three pieces of our program and our code base is as shown below.

{% include_code count_cities.py %}

Looks like writing our first test is easy! We can just directly test the build_query_locations method and ensure it works as we expect. Our second test should be pretty easy too, as we can create some sample responses from Google and make sure we only accept the right ones. The third test though is irritating, since it depends on us actually calling Google's API in our test.

There are a few reasons this external dependency is unfortunate: 

1. It's slow! A round trip query takes in the neighborhood of 700 ms, which means one run of our program will take on the order of half a minute. Gross.
2. It probably doesn't need testing (by us). We generally trust Google to do the right thing. We are currently trying to unit test our own code, and where possible, we should assume that Google's API is a thoroughly tested black box.
3. Our own testing is now more complicated. What happens if I want to test how find_matching_states handles a geocoder result that comes back as `None`? Or a city with accented characters? These are hard to generate if I'm actually calling out to my geocoding library and using the real result.

This is not a comprehensive list, it's merely three issues that apply to this particular block of code. Now imagine how these complaints scale up when you're talking about a commercial webapp and you can start to see why mocking is so important in tests.

### Fine, mocking is good. How do I do it? ###

And now we're to the good stuff -- how to mock out methods in your own tests. Gary Bernhardt wrote up a [comparison](http://garybernhardt.github.com/python-mock-comparison/) of various mocking libraries for python, all of which would work for your purposes. Personally, I've stuck with the mock library and been quite happy with it.

So enough rambling already, let's see this in action. I've written a single test below, aimed at unit testing the find_matching_states method. In particular, note how we manipulate what the `geocode_address` call returns to make our testing simple, while still asserting that we are calling the method with the arguments we expect.

{% include_code count_cities_test.py %}

Note that with this test, the only thing we've stopped testing is the content of Google responses for particular arguments to `geocode_address`. The danger (as always with mocking), is that we actually are uncertain of this response format or contents. If this were the case, we'd want to construct separate tests -- only operating on the `geocode_address` method -- that verified the behavior we required. But in exchange for this, we've replaced a 700ms call with one that takes no time, gained control over the value returned by `geocode_address` and in the case of an API like this, possibly saved ourselves real money! These are very real advantages that become even more valuable when employed at scale.

The simple fact is, you cannot reliably make every test an integration test at scale and -- more importantly -- you shouldn't want to do so. With any luck, this post has pointed out a few advantages of mocking in your tests and explained the overall reasoning behind the choice. All that remains is to pick your library of choice and learn to use it skillfully. And that is all there is to it. There's a ton to learn about how best to use tools like stubs and mocks in your code, but I have been repeatedly impressed by how much they have improved both the clarity and quality of my tests.
