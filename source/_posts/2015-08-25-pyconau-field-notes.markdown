---
layout: post
title: "PyconAU 2015 field notes"
date: 2015-08-25 19:16
comments: true
categories: conferences
---

I was lucky enough to speak at PyconAU 2015, in Brisbane! Least I can do is write up some notes about the talks I particularly enjoyed. Here they lie, somewhat edited and mostly linked against the conference website.

<!-- more -->

It's worth mentioning that PyConAU was really well run and organized, both as a speaker and an attendee. Well worth the trip if you're ever in the area!

## [My talk -- the awkward adolescence of SOA](https://www.youtube.com/watch?v=H0KReHUawHI)

Let's get mine out of the way first. I spoke on what it's like to watch service architecture mature at Yelp...in particular the kind of application challenges you only see in a more mature SOA ecosystem.

I'll leave you to watch the talk, but I think it went pretty well within the time limits. Had some good discussions in the hallway after about the (many) other interesting challenges a system like this faces besides the ones I had time to present. It's an incredibly complex topic, but I was happy to hear from a few separate people who echoed a lot of the difficulties I've experienced in this area.

I should also [link the slightly longer version of this talk](https://www.youtube.com/watch?v=z3_HorshzJ4), which I gave at Europython. It's largely the same content, but with an extra section on keeping systems decoupled.

## [Slow down, compose yourself](http://2015.pycon-au.org/schedule/30126/view_talk?day=saturday)

"Inheritance leads to objects that are simply too big"

Turned into a very testing/mocking/verified fakes heavy talk very quickly. Worth watching in concert w/ the verified fake talk at EuroPython. 

Largest lesson from talk might be that good composition forces exposing seams in your arch that inheritance may hide.


## [Fang: Pythonic dependency injection](http://2015.pycon-au.org/schedule/30114/view_talk?day=saturday)

[Github repo](https://github.com/ncraike/fang)

Definition: code you write doesn't directly refer (or require to be passed) the objects it uses. Most of the discovery and retrieval of such objects is completely magic and done without programmer intervention.

Most popular in Java/C# because of their typing systems being restrictive. 

I found the most interesting part of the talk discussion about why I should even care about DI in python. What about just passing objects around and/or mocking libraries?

* Best use case is testing. Some things you want to mock are never available at the module scope.
* Missing mocks are a definite issue for testing (think scary side-effects like sending email in your testing suite)
* Many people work around this by passing in deps that aren't deps -- see kwargs w/ default args that are never actually used.

## [To AST and Beyond](http://2015.pycon-au.org/schedule/30046/view_talk?day=saturday)

Cool talk, chiefly about tooling surrounding the Python AST. Most important things I learned about were these projects:

* [Python AST module](https://docs.python.org/2/library/ast.html)
* [Green Tree Snakes](https://greentreesnakes.readthedocs.org/en/latest/)
* [Astor](https://github.com/berkerpeksag/astor)


## [Breaking Backwards Compatibility](http://2015.pycon-au.org/schedule/30062/view_talk?day=saturday)

My team at Yelp maintains a public-facing API, so this one was particularly interesting. Lots of good discussion of the various aspects of maintaining a public, changing interface.

Versioning:

* Differentiates versions of the software. Allows users to be aware of what they're interacting with.
* Allows you to publish timelines and release schedules. Give expectations about when changes are going to happen.
* Allows planned deprecation of old features/behaviors. 


Communication:

* Be clear when features are being deprecated or removed.
* Make deprecation notices at least one cycle in advance (e.g. a deprecation warning release and then a later removal major-version bump)
* Have a well defined (stable process!) release cycle
* Communicate clearly with your users. Changelogs, even guides for major changes...make sure they know all of this.


Consistency:

* Consistency in your API does wonders for its adoption and ease-of-use
* Helps make large breaking changes go easier (reduces cognitive overhead)
* Consider even providing contracts in your API (like SLAs? connection w/ acceptance tests)


Privacy:

* Private by default
* Be cautious of what you expose to the outside world. Once you do, it goes from implementation detail to part of your public interface. 
* Once it is public, you have to assume it's being used in the most awful/strange ways possible


Testing:

* Acceptance testing is extremely important
* Test cross-version where possible
* Cross-version monitoring/canarying?


## Keynote: Consequences of an Insightful Algorithm

Very high level talk about the negative impact of the algorithms on our users. How can we write algorithms and perceive insights without losing our empathy? Without hurting our users?

False positives and negatives have human consequences when deployed on people. Just having a low rate of FP isn't enough if FP have particularly harmful effects.

Academic studies have tons of oversight and checks/balances. Industry needs to make sure it's not doing wildly unethical things in the name of progress.

Increase awareness of edge cases, failure modes, and worst case scenarios. Be humble and admit that we cannot know everything about the users we are interacting with. 

Huge asks. Huge awareness of consequences.

## [Make your logs work for you](http://2015.pycon-au.org/schedule/30012/view_talk?day=sunday)

Pretty high level overview of the ELK stack. Went into some detail on each part of it. 

Recommends that, as your data gets older, you should snapshot it, move to weaker boxes, and eventually delete entirely. Advocates for daily indices to make this easier.

Referenced [entity centric indexing](https://vimeo.com/elasticsearch/review/107682325/6c999f47b4) talk as relevant.
