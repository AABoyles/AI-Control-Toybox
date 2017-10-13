# Control Problem

The Control problem is a trivial example of a way in which an autonomous system can develop malign behaviors if its reward function doesn't match its creators' utility function.

The gist of it is a robot who can push boxes around a grid of squares. It is intended to push one box into a hole, and to do so efficiently. However, its utility function doesn't match its creators': specifically, there are multiple boxes, and it receives a utilon for each box it puts into the hole. To assure this doesn't happen, there's a security camera with a direct line-of-sight to the hole.

It was first described on [LessWrong in 2015](http://lesswrong.com/lw/mrp/a_toy_model_of_the_control_problem/).

[Motivating Post](https://www.lesserwrong.com/posts/EdEhGPEJi6dueQXv2/toy-model-of-the-ai-control-problem-animated-version)

[Original Code](https://www.dropbox.com/sh/bflmein9d9oxjxe/AAA_A2AwQQJ00kveKDPEpsRea?dl=0)

[Explanatory Video](https://www.youtube.com/watch?v=sx8JkdbNgdU)

In addition to the relevant code, this repository also contains the complete set of [output]('output/') from the script.
