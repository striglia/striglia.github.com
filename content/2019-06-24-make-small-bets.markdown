---
Title: Make more bets, make them smaller, re-invest in what works
Date: 2019-06-24
Category: roadmaps
---


As you go from coding from specs, to designing project plans, to building team roadmaps, to leading groups, there is a consistent theme of getting more comfortable with handling uncertainty. It goes from something you rarely have to think about to an omnipresent part of work life. Feedback loops take longer to return a signal on what's working, and the signal you do get is increasingly muddy and uncertain.

As you tackle more uncertainty (about the future, about the project requirements, about how you're going to solve your task), it's extremely easy to get stuck in [analysis paralysis](https://en.wikipedia.org/wiki/Analysis_paralysis) -- when the complexity of factors to consider makes you unable to actually make a choice in the end. One of the key skills to grow as a technical lead (or any wide-scope leader) is being able to take an incredibly complex problem and still make forward motion on it.

I've written about this before from [the perspective of iterated bets](https://medium.com/@scott_triglia/ask-a-tech-lead-i-have-to-make-a-technical-decision-but-i-cant-know-the-right-answer-4c674f9f4a74) and roughly suggested applying the scientific method. But recently talking through my own approach to problems like this I realized there's another angle I left out - making many bets in parallel.

### Acting like a lean startup

One of the realities of the tech business is that the space we play in, all potential things we could build, is mind bogglingly large. We cannot possibly know before hand the right choices to make -- the only option is to discover as we go.

Lucky for us, this concept of testing our theories out cheaply, seeing how they perform in the marketplace, and iterating based on the feedback we get is a well-explored topic in startup literature. If you want to read in more detail, I recommend [the Lean Startup](http://theleanstartup.com), which promotes the following familiar principles:

* Failing fast and cheap -- try to quickly get feedback before you invest tons of time into a plan. Will it work in practice?
* Develop an MVP -- don't gold plate your idea until it's been trialed in real life
* Validated learning -- get your product (in my case, usually technical/process/culture changes) out there and get feedback from customers.

It is valuable to think of your org (team, group, or larger) in this "startup" framework. Particularly for infrastructure/platform teams, there's a dangerous entropic pull toward an unhealthy "we build technology X" and away from a more solution oriented "we solve our customers problems". Focusing on cheap experiments teaches you about your market, what works, and where to direct your future investments.

### Betting (and learning) in parallel

This brings us back to the title of the post -- making lots of small bets.

My Medium post was written about major "fork in the road" choices (should I use technology A or B) that have bets which are inherently serialized. You need to pick a particular direction, but there aren't usually multiple simultaneous bets in progress.

In contrast, if I'm thinking of how best to lead a team or group, I want to have a number of different irons in the fire at the same time. Some might be more process oriented ("make oncall more sustainable"), others more technical ("establish a unified interface for our platform"), and others cultural ("foster technical leadership/roadmaps at the team level").

I prefer to have a number of these in progress at once. By necessity, this means I'm probably being less of a personal owner of each effort, and more of a program manager -- making sure some other owners are moving forward with each one, ensuring they're all advancing a coherent agenda.

### Ensuring your various bets all advance the same goal

The main downside of making multiple small bets instead of one big one is fragmentation -- it's much easier to not be working in a consistent direction toward a single goal. This is true when making many small technical bets and it's equally true of the individual efforts of people or teams in your group.

You can move mountains when you have many efforts aligned in the same direction, but you might also have your own efforts fighting each other and accomplish nothing. The key is to ensure your bets are all consistent, advancing the same agenda in a coherent direction.

[One of my favorite explanations of this idea is this article/talk](https://thinkgrowth.org/what-elon-musk-taught-me-about-growing-a-business-c2c173f5bff3), which expands on a quote originally from Elon Musk: "Every person in your company is a vector. Your progress is determined by the sum of all vectors."

In my own technical work, building this alignment usually looks like the following orientation documents:

* A charter -- one or two pages that lays out my groups mission and orients us toward major challenges
* A roadmap -- a technical plan for major themes of work over the next 6-24 months
* A target architecture -- a map of how we want to think about the inter-relations of systems we own, and in particular their public interfaces to the world outside our group

It's a funny thing -- none of these three documents are necessarily earth shattering on their own. You might very well read the charter and think "well of course that's what we do", or see the roadmap and say "sounds about right". The target architecture often falls out of date and needs updating regularly.

But the beauty of these artifacts is they are still excellent at building and maintaining alignment. They're all ways of helping point our team's vectors in a consistent direction.

### Identifying the right small bets for you

This all brings us to that important choice -- what bets should you pursue first?

[I'm a big believer in immersing yourself in the problem space, identifying concrete next steps, executing on them, and repeating.](https://twitter.com/scott_triglia/status/1017453906207571968) For my own bets, they often end up being these "first steps" along various avenues identified in my technical roadmap or target architecture. It's often pretty easy to generally say "an interface between systems A and B needs to exist" or "oncall needs to be more sustainable", which helps focus attention and turn the problem from "what area should I work on" to "what's the right first step in this particular area".

Again, the safety net here is that **your choices and bets don't need to be 100% correct to be useful**. Any attempt will give you a feedback signal on the ROI for investing further, which can help you better position future bets.

In total:

1. Build deep context in your area
2. Form a few opinions about where opportunity lies
3. Place your small bets across some of these opportunities
4. See which ones pay out, which ones fail, and update your belief about future opportunity
5. Repeat!

If you have thoughts on how you attack the "where to invest" problem, or more detailed questions, I'd love to hear about them [on Twitter at @scott_triglia](https://twitter.com/scott_triglia).


