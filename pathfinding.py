from queue import Queue as q
import config
import time
from snap_to_grid import SnaptoGrid
import heapq
import sys
import pygame

sys.setrecursionlimit(10000)
dfs_route = None

class Queue(q):
	def __repr__(self):
		return f"Queue({self._qsize()})"

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def __repr__(self):
    	return f"PriorityQueue({len(self.elements)})"
    
    def empty(self):
        return not len(self.elements)
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def peek(self):
    	return self.elements[len(self.elements)-1]
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Pathfinding:
	'''set up grid, pathfinding algorithms'''
	def __init__(self, nodes, weights):
		self.nodes = nodes #all available movement positions (objs are removed from here in map generation)
		self.square = config.grid_spacing
		self.weights = weights

	def compute_all_paths(self,start_x,start_y,end_x,end_y):
		'''use mouse to select path endpoint and compute routes for BFS, GBFS, DA, A*'''
		end_x = SnaptoGrid.snap(end_x)
		end_y = SnaptoGrid.snap(end_y)
		start = (start_x,start_y)
		end = (end_x,end_y)

		print(f'Computing routes from {start} to {end}\n')

		routes = {'BFS':None, 'DFS':None, 'GBFS':None, 'DA':None,'A*':None}

		for route in routes.keys():
			start_time = time.time()
			if route == 'BFS':
				node_path = self.breadth_first_search(start, end)
			elif route == 'DFS':
				print('computing Depth First Search route...')
				self.depth_first_search(start, start, end, {start:None})
				node_path = dfs_route
			elif route == 'GBFS':
				node_path = self.best_first_search(start, end)
			else:
				node_path = self.dijkstra_search(start, end, True if route=='A*' else False)
			if not node_path:
				break
			print(f'{route} took {round(time.time() - start_time, 4)} seconds. Nodes to traverse: {len(node_path)}.\n')
			routes[route] = node_path
		
		return routes if node_path else None

	#relative cost for moving on diff sqaures. Normal = 1, grass = 2, water = 5
	def movement_cost(self, node):
		return self.weights.get(node, 1)

	#heuristic is just the straight line distance between the end (x,y) and (x,y) of a possible next node
	#GBFS and A* algorithims seeks to minimise this by adding it as a cost
	def heuristic(self, end, next_node):
		(x1, y1) = end
		(x2, y2) = next_node
		return abs(x1 - x2) + abs(y1 - y2)

	def neighbours(self, node):
		#East, South, West, North
		dirs = [[self.square, 0], [0, self.square], [-self.square, 0], [0, -self.square]]
		result = []
		for dir in dirs:
			neighbour = (node[0] + dir[0], node[1] + dir[1])
			if neighbour in self.nodes: 
				result.append(neighbour)		
		return result

	def breadth_first_search(self, start, end):
		print('computing Breadth First Search route...')
		positions = Queue()
		positions.put(start) #enqueue start
		previous_positions = {}
		previous_positions[start] = None

		while not positions.empty():
			current_pos = positions.get()
			
			if current_pos == end: #found end, stop searching
				print(positions)
				break

			for next_pos in self.neighbours(current_pos):
				if next_pos not in previous_positions:
					positions.put(next_pos)
					previous_positions[next_pos] = current_pos

		return self.get_path_back(start, end, previous_positions)


	def depth_first_search(self, start, current_pos, end, previous_positions):
		if current_pos == end:
			global dfs_route
			dfs_route = self.get_path_back(start, end, previous_positions)
			return

		for next_pos in self.neighbours(current_pos):
			if next_pos not in previous_positions:
				previous_positions[next_pos] = current_pos
				self.depth_first_search(start, next_pos, end, previous_positions)


	def best_first_search(self, start, end):
		print(f'computing Greedy Best First Search route...')
		positions = PriorityQueue()
		positions.put(start, self.heuristic(end, start))
		previous_positions = {}
		previous_positions[start] = None

		while not positions.empty():
			current_pos = positions.get()
			
			if current_pos == end:
				print(positions)
				break

			for next_pos in self.neighbours(current_pos):
				#havnt calculated cost for next pos or found a better route
				if next_pos not in previous_positions:
					priority = self.heuristic(end, next_pos)
					positions.put(next_pos, priority)
					previous_positions[next_pos] = current_pos
		
		return self.get_path_back(start, end, previous_positions)


	def dijkstra_search(self, start, end, a_star=False):
		print(f'computing {"Dijkstra" if not a_star else "A*"} route...')
		positions = PriorityQueue()
		positions.put(start, 0 if not a_star else self.heuristic(end,start))
		previous_positions = {}
		previous_positions[start] = None
		cost_so_far = {}
		cost_so_far[start] = 0 if not a_star else self.heuristic(end,start)

		while not positions.empty():
			current_pos = positions.get()

			if current_pos == end:
				print(positions)
				break

			for next_pos in self.neighbours(current_pos):
				#cost of movement is the current cost of movement + cost of moving to next code
				new_cost = cost_so_far[current_pos] + self.movement_cost(next_pos)
				#if new cost of movement is less than prev cost of movement to that node, enqueue the node
				#if we havn't checked the next node, also enqueue it - we can check it again later
				if new_cost < cost_so_far.get(next_pos, sys.maxsize):
					cost_so_far[next_pos] = new_cost
					priority = new_cost + self.heuristic(end, next_pos) if a_star else new_cost
					positions.put(next_pos, priority)
					previous_positions[next_pos] = current_pos

		return self.get_path_back(start, end, previous_positions)


	#reverse the path from end to start so we can map it
	def get_path_back(self, start, end, previous_positions):
		path = []
		path_back = end
		try:
			while path_back != start:
				path.append(path_back)
				path_back = previous_positions[path_back]
			path.reverse()

			return path
		except:
			print('no path exists')