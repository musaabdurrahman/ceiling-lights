
## The Problem:

A ceiling is made up of discrete blocks and populated with lights (that take up a full block) at regular intervals. The lights must be placed such that the first light and the last light are the same distance to the first wall and the last wall respectively, and then every light in between is placed at regular intervals.

![Diagram showing the blocks, gaps, distance from wall,and total length](diagram.png)

Given a certain dimension $D$ and gap $g$, we need to find a distance from the wall $w$ and number of lights $n$ that will ensure the ceiling lines up.

For example, a 31 block wide ceiling with a gap of 5 empty spaces between each light would work with a margin of 3 at each wall because:
$$
3+1+5+1+5+1+5+1+5+1+3=31
$$

## The Equation:

Any valid configuration of lights must satisfy the equation:
$$
D = 2w + n +(n-1)g
$$
This is simply because 