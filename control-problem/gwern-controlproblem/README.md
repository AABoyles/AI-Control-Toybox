# Gwern's Control Problem

The Control problem is a trivial example of a way in which an autonomous system can develop malign behaviors if its reward function doesn't match its creators' utility function.

The gist of it is a robot who can push boxes around a grid of squares. It is intended to push one box into a hole, and to do so efficiently. However, its utility function doesn't match its creators': specifically, there are multiple boxes, and it receives a utilon for each box it puts into the hole. To assure this doesn't happen, there's a security camera with a direct line-of-sight to the hole.

It was first described on [LessWrong in 2015](http://lesswrong.com/lw/mrp/a_toy_model_of_the_control_problem/). In response to that LessWrong post, Gwern and FeepingCreature developed [a rudimentary demo of the problem](http://www.gwern.net/docs/rl/armstrong-controlproblem/index.html).

## License

Gwern's content [seems to be licensed](http://www.gwern.net/About#license) under the [CC-0 Public domain](http://creativecommons.org/about/cc0) license. However, I have not consulted with him about mirroring this project here, and as I do for all the non-original projects in this repository, I precommit to remove this at his request (or the request of anyone else who can offer a credible claim of ownership over this work).
