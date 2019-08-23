---
Title: Why you should use Black for your Python style linting
Date: 2019-08-23
Category: python
---


_This was written in early 2019 as an internal proposal for why Yelp should adopt Python's Black library for style linting. The document’s style is heavily modeled after Amazon’s 6 pagers ([detail here](https://medium.com/@inowland/using-6-page-and-2-page-documents-to-make-organizational-decisions-3216badde909)). It's early to declare whether that effort worked or not (though early feedback was positive), but while writing this up I felt there were too few public position papers advocating for Black usage. So here's at least one more, in case it is useful to others._

## Document Purpose

Decide if our various current Python style linting solutions (autopep8, pylint, flake8) should be replaced or simplified with an opinionated auto-formatter library called Black.

## Background

Historically, we have always had a recommended Python style. Originally this was a wiki page, then various levels of [automated linting](https://en.wikipedia.org/wiki/Lint_(software)) including different combinations and configurations of tools like autopep8, flake8, and pylint. 

There’s significant overlap within these tools, but roughly they break down into a few areas of focus:

1. Pycodestyle: identifies [pep8](https://www.python.org/dev/peps/pep-0008/) style violations
2. autopep8: automatically fixes most violations identified by pycodestyle
3. [Add-trailing-comma](https://github.com/asottile/add-trailing-comma), a precommit hook that does various style enforcing (not just trailing commas). 
4. Pylint: throws warnings or errors for a combination of programming and style issues
5. Pyflakes: similar to pylint, except _never_ complains about style
6. Flake8: wraps pyflakes and pycodestyle; roughly combines the two

Empirically, we largely seem to have standardized on the pair of flake8 and autopep8, though with lots of variation in their configuration.

We use [pre-commit](https://pre-commit.com/) to enforce most of these linting solutions at the time of git commit. Pre-commit itself has [a large set of additional optional hooks](https://pre-commit.com/hooks.html), many of which solve individual style problems (e.g. bad indentation). 

Other languages have seen a movement toward minimally configurable, autoformatting solutions: Go started it [with gofmt](https://golang.org/cmd/gofmt/) and JS [has prettier](https://prettier.io/ ). They’ve both seen successful adoption because they are simple to use, remove formatting as a bikeshed issue, and generally let you focus on the actual code you’re writing, not manual adherence to best practices.

[Python has an equivalent library called black](https://black.readthedocs.io/en/stable/index.html). It has seen growing popularity within the Python community, including adoption and recommendation from major repos ([attrs](https://github.com/python-attrs/attrs/blob/master/.pre-commit-config.yaml#L2) and [django](https://github.com/pydanny/cookiecutter-django/issues/1601)) and testimonials [from very experienced Python developers](https://black.readthedocs.io/en/stable/index.html). The library bakes in opinionated enforcement of PEP8 and some additional best practices,[ explained in more detail here](https://black.readthedocs.io/en/stable/the_black_code_style.html).


## Problem

We do not use black for Python and many of our current Python linting solutions present with various problems.

Significant pain points with our status quo are inconsistency of configuration and manual resolution of errors. Both of these are addressed by adopting an auto-formatting linter like black.


#### Inconsistency

Unfortunately, we apply style linters inconsistently across our repos. Some of these happen in tox files, some in pre-commit config, some in both. 

Even if we agree which tools to use, each of them supports a tremendous amount of configurability (see [autopep8](https://pypi.org/project/autopep8/#id3) and [flake8](http://flake8.pycqa.org/en/latest/user/options.html) documentation). This produces lots of variation in practice and demands more choices about what is or isn’t best style. In practice, there is no common agreed choices for all these values.

In the end, this inconsistency across repos makes collaboration, team changes, and onboarding new hires all harder than necessary. 


#### Manual resolution of errors

As a general rule, these tools do not all consistently fix problems they identify. Autopep8 is the closest, but it is also the most narrowly scoped.

Any case of linters only _identifying_ style issues leaves developers to manual resolve them, often only after an attempted `git commit` or `make test` fails at the last step.

Some style linting issues (e.g. breaking up a long function signature) are only partially enforced by tools like flake8, resulting in lots of style nitpicks at code review time. This produces extra work for all involved and can be a source of disagreement between engineers where our style guides are unclear. 

Finally, the manual resolution still leaves opportunity for minor differences in actual solved states since the linters tend to only forbid the worst offences (e.g. 150 character function signature lines) instead of enforcing a consistent solution (e.g. always splitting long function signatures onto one line per argument).


## Possible Solutions

Like the library it recommends, this whitepaper is opinionated -- we should standardize our various style linters and only use black. That said, there are still options for how we should go about it.

The main choice seems to be around how aggressive we are about accepting black’s default configuration.

Note that for a variety of non-style linting concerns, we should run flake8 after Black. From the Black documentation, this would look like a flake8 configuration of:


```
    [flake8]
    select = C,E,F,W,B,B950
    extend-ignore = E501
```


#### Black with default configuration

The simplest solution -- just run Black with zero configuration. This accepts all of Black’s opinions as correct and in return gives us an extremely simple setup and mental model. 

We can run as a pre-commit hook with only a few lines:


```
    -   repo: https://github.com/ambv/black
        rev: stable
        hooks:
        - id: black
          language_version: python3.6
```


Black auto-detects the python version of the file under linting, so this should work in both Python 2 and 3 repos.


#### Black with per-repo configuration

We can also choose to roll out Black with some use of its limited configurable opinions. The most interesting of these is modifying line length and its standardization of double quotes.

`--line-length` would allow us to alter the default of 88 character cutoff. The advantage here seems minimal (this was picked wisely, using empirical data), but it is an option to allow 120 chars or something similar.

`--skip-string-normalization` would allow single quoted strings (instead of Black’s default of enforcing only double quotes). This is one of the most controversial opinions of Black and may be a source of strong resistance to the change. Using this flag loosens the consistency of our codebase, but may help avoid controversy with this proposal.

Note that if we change these settings per repo, we’ll also need to keep flake8 config consistent. This introduces an additional slight amount of upkeep. 

For this option, we’d likely leave these settings to the discretion of each repo, with the encouragement being “use Black’s defaults unless you feel extremely strongly”.


## Recommended Solution

Let’s use Black as a pre-commit hook with standard (default) configuration, alongside flake8 for non-style linting.

The fact that Black contains some individual controversial choices (e.g. standardizing on double quotes for strings) is overwhelmed by the value of automating style nitpicks away and offering all our engineers a consistent, open-source standardized style across repos.

For a more detailed argument in favor of this approach, [see the Django project’s reasoning for the same choice.](https://github.com/django/deps/blob/master/accepted/0008-black.rst)

If it feels useful, we can also include documentation and evangelizing [of native IDE integrations](https://black.readthedocs.io/en/stable/editor_integration.html) for black.

Documentation should be central and include:

*   This document explaining the motivation behind the change
*   Links to [https://black.readthedocs.io/en/stable/the_black_code_style.html](https://black.readthedocs.io/en/stable/the_black_code_style.html), which has a FAQ for the most common questions about “why is black choosing to do this particular change”.
*   Probably at least one external reference of choice like [https://www.mattlayman.com/blog/2018/python-code-black/](https://www.mattlayman.com/blog/2018/python-code-black/) or [https://prettier.io/docs/en/why-prettier.html](https://prettier.io/docs/en/why-prettier.html) which gives more context on benefits.


## Proposed plan of action

Make the central wiki page described above.

Select two small, low-developer-count repos and get social buy in to trial this proposal. Like most linting choices, this is not an easily reversed choice once applied but we can at least use `pre-commit run --all-files` to apply the style changes in a single, easily identified git commit. If desired, we can make the commit as a special one-off git author to make this change more obvious when viewing git history later.

If the small repo rollouts reports positive or neutral developer happiness, measured via a brief survey, we can progress wider. More general rollout should likely follow the same rollout strategy as initial repos, including any best practices learned.

If all goes extremely well and momentum builds, eventually we should 1) standardize this as the standard, recommended solution, and 2) apply this same process everywhere.

Anticipating a concern: [the current “Beta”](https://black.readthedocs.io/en/stable/installation_and_usage.html#note-this-is-a-beta-product) disclaimer should be removed soon according to the Black maintainer ([source](https://github.com/python/black/issues/517)). We’d presumably wait for this step to be official before completing any full rollout.


## Appendix -- Prettier’s take on why you should use an auto-formatter

Prettier (the JS equivalent of Black) has a tremendous “why use Prettier” page explaining their philosophy and justification. It is at [https://prettier.io/docs/en/why-prettier.html](https://prettier.io/docs/en/why-prettier.html)  and you are strongly recommended to read it.


## Appendix -- Discussion from HN with relevant excerpts

Original discussion: [https://news.ycombinator.com/item?id=19939806](https://news.ycombinator.com/item?id=19939806). General sentiment of people who had used it long term seems positive.

[(source)](https://news.ycombinator.com/item?id=19942253) I was initially grumpy about my org adopting black because I preferred single quotes, but the level of standardization is a huge win in my book. I never even think about my code style anymore, I just write it and then run black.


[(source)](https://news.ycombinator.com/item?id=19941182) if the progress of prettier (js) over the past few years is any indicator of what will happen with black, there will likely be incremental improvements in black that address the poor formatting cases you’re concerned about. i remember when prettier first came out, i was not convinced until my “standard” for formatting was met. but it was met eventually.


[(source)](https://news.ycombinator.com/item?id=19941124) While I agree that [this particular] formatting choice looks a little weird. The primary benefit of a formatter is that the formatting is always the same not. It's less important that it matches everyone's preferences and more important that it always formats the code the same way.


[(source)](https://news.ycombinator.com/item?id=19941119) I often dislike autoformatter output too, but then I remember that while no-one likes what the autoformatter does to _their_ code, everyone likes what the autoformatter does to their coworkers' code, and then I chill out about it.

Having a standard is more important than the standard being excellent.


[(source)](https://news.ycombinator.com/item?id=19941321) Let me take a shot at why it's important. We spend years peering at code hunting for tiny, miniscule mistakes. Thus we're training ourselves, quite rigorously, to spot minor deviations.

We're also irrational in the moment: our aesthetic sense is bothered by certain patterns, and our social sense wants to assign blame for this "wrongness" to individuals.

An auto-formatter removes a ton of deviations that don't matter, and desocializes the aesthetics. This saves code reviewers time and stress and helps them focus on what actually matters in the code.


[(source)](https://news.ycombinator.com/item?id=19941284) There's a tiny but existent cost that's incurred every time formatting rules that aren't diff-stable result in a noisy code review that takes longer to read, or makes it harder for reviewers to discern the real changes from the formatting junk. There's a tiny but existent cost when excess delta makes it harder to gitblame. There's a tiny but existent cost when people have to stop and think about how to format their code manually. Or when they have to stop and debate formatting. Or when they read someone else's code slightly more slowly because different formatting rules make it harder for them to skim it or rely on pattern recognition instead of careful reading to understand its structure.

All those tiny little costs add up to something that's not so tiny. And it's so easy to make it just disappear, for the low low cost of swallowing one's pride, by simply adopting an opinionated autoformatter.


[(source)](https://news.ycombinator.com/item?id=19940767) The way you can tell that black is good is that everyone mildly dislikes a few things about it, but they're usually different things.

That's usually a good clue that you've hit real middle-ground. I blackify my projects once we hit 3 contributors.


[(source)](https://news.ycombinator.com/item?id=19941466) I like auto-formatting, because it makes PRs less stressful to commit, and makes review comments more focused on stuff that actually matters. How exactly the code gets formatted is not something I care much about, just that it happens consistently, and I don't have to think about it.

