# Pathfinding

Description:
This project is an interactive game designed to visually show the differences between different graph traversal algorithms, particularly, differences in running time and in chosen routes taken.

The game graphically compute paths between pairs of start and end coordinates using various graph traversal algorithms including: Breadth First Search, Depth First Search, Greedy Best First Search, Dijkstra's Algorithm and A* Algorithm.

# How to Use

Run game_pathfinding.py

Use the Arrow Keys to move the player around the map. Press the mouse button to compute paths between the players (x,y) coordinates and the (x,y) coordinates of the mouse. 

One can play around with the window dimensions in config.py and use the generate_map() function in map_generation.py by passing in a list of sprites to generate new maps of different sizes with varying numbers of different obstacles at random locations.

Obstacles such as trees and buildings cannot be walked through, whereas grass and water is traversable yet incurs a movement cost to the player (reduced movement speed).

# Requirements

- python3.7
- pygame
