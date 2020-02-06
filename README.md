# Artifitial Intelligence Project

Projects:

- Constrain Satisfaction Problem
- Map Coloring
- Rubik's Cube
- Text Classification

## Constrain Satisfaction Problem
In this project we use csp techniques to solve the following problem.

Imagine a graph whose nodes are either Triangle, Square, Circle, Pentagon or Hexagon. The aim is to assign values in range 1 to 9 to each node such that following conditions hold:

1. Value of each Triangle node must equal to the left most digit of the multiplication of its neighbors.
2. Value of each Square node must equal to the right most digit of the multiplication of its neighbors.
3. Value of each Pentagon node must equal to the left most digit of the summation of its neighbors.
4. Value of each Hexagon node must equal to the right most digit of the summation of its neighbors.
5. A Circle node can have any value in range 1 to 9

## Map Coloring
Given an uncolored graph (usually map of a county) and a number of legal colors assign a valid color to each node such that no adjacent nodes have the same color.

This problem is solved using 2 local search algorithms.

1. Genetic Algorithm
2. Simulated Annealing Algorithm

## Rubik's Cube
Given a 2\*2\*2 rubik's cube instance find the minimum number of moves required to solve it.

This problem is solved using 3 search algorithms.
1. Iterative Deepening Search (IDS)
2. Bidrectional BFS
3. UCS Algorithm (basically just a BFS)

## Text Classification
Using a set of sample texts (training data) that each of them belongs to a specific subject we build two different models (unigram and bigram) and we use them to predict the class of a given text. (test data)