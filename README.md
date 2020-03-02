# Pathfinding

Description:
This project is an interactive game designed to visually show the differences between different graph traversal algorithms, particularly, differences in running time and in chosen routes taken.

The game graphically compute paths between pairs of start and end coordinates using various graph traversal algorithms including: Breadth First Search, Depth First Search, Greedy Best First Search, Dijkstra's Algorithm and A* Algorithm.

# How to Use

Run game_pathfinding.py

Use the Arrow Keys to move the player around the map. Press the mouse button to compute paths between the players (x,y) coordinates and the (x,y) coordinates of the mouse. 

One can play around with the window dimensions in config.py and use the generate_map() function in map_generation.py by passing in a list of sprites to generate new maps of different sizes with varying numbers of different obstacles at random locations.

Obstacles such as trees and buildings cannot be walked through, whereas grass and water is traversable yet incurs a movement cost to the player (reduced movement speed).

If you want to change which routes are computed, comment out the relevant route being draw in redraw_gamewindow() in game_pathfinding.py and route being computed in compute_all_paths() in pathfinding.py.

# Requirements

- python3.7
- pygame

# Screenshots and Detail

## Breadth First Search (Blue):

Uses a Queue and expands outwards in all directions to find shortest path.
![pf_bfs](https://user-images.githubusercontent.com/31314787/75724880-34b19a00-5cd7-11ea-8614-db2aef8aa44e.PNG)

## Greedy Best First Search (Red):

Uses a Priority Queue and seeks to minimise the distance between the goal and current node being search to find a path (not necessarily the shortest). Nodes further from the goal are given a lower priority than those closer to the goal.
![pf_gbfs](https://user-images.githubusercontent.com/31314787/75724893-3bd8a800-5cd7-11ea-90a1-d39a3024186d.PNG)


## Dijkstra's Algorithm (Green) and A* (Grey):

DA uses a Priority Queue to find the shortest path and allows for 'weights' to be assigned to certain nodes to take into account routes which may be faster / slower despite being further / closer to the goal. In this game, grass and water are assigned heavy movement weights and so DA avoids these areas (unlike BFS/GBFS).

A* uses a combination of GBFS and A* to prioritise routes which are in the general direction of the goal. A* generally runs
faster than DA, although in this case, A* sometimes overshoots (overestimates distance to goal) and finds a slower route (more nodes to traverse) than DA. This is because in this implementation A* just seeks to minimise the straight line distance (as the crow flies) between the current node being search and the end goal -> this does not take into account any obstacles which may be in the way and hence sometimes overshoots (particularly if there are lots of obstacles).
![pf_da_astar](https://user-images.githubusercontent.com/31314787/75724898-3f6c2f00-5cd7-11ea-966c-b684d0407a85.PNG)


## Depth First Search (Dark Blue):

DFS is by far the slowest of all these methods to find a route to a goal. It searches lazily in one direction and backtracks
to search in another direction when it reaches a dead end. It does not stop until it finds the end goal. This algorithim is especially
slow where there are few obstacles as there are few dead ends. It will only run on larger or emptier maps by overriding the system maximum recursion depth.

![pf_dfs](https://user-images.githubusercontent.com/31314787/75724909-43984c80-5cd7-11ea-8360-351ef97bfc41.PNG)
![pf_all](https://user-images.githubusercontent.com/31314787/75724918-47c46a00-5cd7-11ea-8902-a54a90fe2807.PNG)
![pf_all2](https://user-images.githubusercontent.com/31314787/75724923-4abf5a80-5cd7-11ea-972a-05467f459163.PNG)

![pf_all2_console_output](https://user-images.githubusercontent.com/31314787/75726619-bbb44180-5cda-11ea-93a5-40e6c9d40e5b.PNG)
