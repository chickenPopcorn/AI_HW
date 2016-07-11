# HW2 AI FOR 2048

The current implementation is consistent with the specification for homework 2. It completes a move using less than 1 sec using adversarial search algorithm specifically minimax with alpha beta pruning

`PlayerAI.py` and its subsequence modules including `MiniMax.py` and `Heuristic.py` are included in this zip file.

The PlayerAI.py is implemented using minimax search algorithm with alpha beta pruning. I also implemented the plain vanilla minimax
and created a test function `testMiniMaxAlphabeta(g)` in `MiniMax.py` to test the correctness of my alpha beta pruning.

I also implemented iterative deepening for my minimax with alpha beta pruning. Instead of starting from depth 0, I set the default depth to be 4 to speed things up, since in my test depth of 4 has never exceed the 1 sec time limit. Most of the time it reached depth of 5 or 6, but when there were less open space the depth can reach as high as 12+.

For the heuristics I tried two different Heuristic functions with their outputs recorded in file `output-test1.txt` and `output-test2.txt`. I started by building function that evaluate grid's smoothness, monotonicity, max tile that is on edge and etc. However its performance is sub-par. It's performance is shown below.
```
-----------------------------------------------
40 test runs stats
% of the games reached 256 and above: 100.0%
% of the games reached 512 and above: 97.5%
% of the games reached 1024 and above: 75.0%
% of the games reached 2048 and above: 10.0%
% of the games reached 4096 and above: 2.5%
-----------------------------------------------
```
Then I moved to all shapes gradient, because it can be implemented and tweaked easily. I ended up using a gradient that is a modified version of ripple effect. Example of the gradient is shown below.
```
[(9, 8, 7, 6),
 (7, 6, 5, 4),
 (5, 4, 3, 2),
 (3, 2, 1, 0)]
```
I also decided to include its mirror image and their 90-degree rotations, because the grid is symmetrical so all eight gradients I used should be valid when evaluating. This heuristic function ending up achieving much better result, which is on par with professor's expectation.
```
-----------------------------------------------
40 test runs stats
% of the games reached 512 and above: 100.0%
% of the games reached 1024 and above: 95.0%
% of the games reached 2048 and above: 52.5%
% of the games reached 4096 and above: 10.0%

-----------------------------------------------
```

