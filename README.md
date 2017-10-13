# AI Control Toybox

A Collection of toy models of AI controls and other instructive things.

I've had the idea rattling around in my head for awhile that someone (me) should archive some of this code that apparently isn't in repositories.

These are the projects, in no particular order.

## The Control Problem

The Control problem is a trivial example of a way in which an autonomous system can develop malign behaviors if its reward function doesn't match its creators' utility function.

The gist of it is a robot who can push boxes around a grid of squares. It is intended to push one box into a hole, and to do so efficiently. However, its utility function doesn't match its creators': specifically, there are multiple boxes, and it receives a utilon for each box it puts into the hole. To assure this doesn't happen, there's a security camera with a direct line-of-sight to the hole.

It was first described on [LessWrong in 2015](http://lesswrong.com/lw/mrp/a_toy_model_of_the_control_problem/).

### Gwern's Control Problem

In response to that LessWrong post, Gwern and FeepingCreature developed [a rudimentary demo of the problem](http://www.gwern.net/docs/rl/armstrong-controlproblem/index.html).

### Armstrong's Control Problem

Stuart Armstrong (the original author of the experiment) was not satisfied that Gwern's implementation exhibited the behaviors he wanted to demonstrate, so he [created his own implementation](https://www.lesserwrong.com/posts/EdEhGPEJi6dueQXv2/toy-model-of-the-ai-control-problem-animated-version).

## The Big Red Button

Following the publication of ["Safely Interruptible Agents"](http://intelligence.org/files/Interruptibility.pdf) (of which Stuart Armstrong was a co-author), Mark Reidl designed [an experiment](https://markriedl.github.io/big-red-button/) (which does not implement the algorithm given by the paper).

Note that this *is* a repository, so I've opted to simply include it as a submodule, rather than copy its contents.

## A note on licensing

I have attempted to respect the licensing of every project archived in this repository. If any of the authors of this material feels that its presence in this repository violates their intellectual property rights in any way, I will remove the offending material immediately without legal intervention. [Please just ask](mailto:aaboyles@gmail.com).

Anything generated in this repository by me (e.g. most of the READMEs) should be considered to be licensed under [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/) or the least restrictive license compatible with the associated project, as required by the license for that project. Basically, I don't care what you do with this stuff, but *I don't own it* so please *respect whomever does*.
