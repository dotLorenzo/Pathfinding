import pygame
from snap_to_grid import SnaptoGrid
import config
from map_generation import Map
from random import choice
import config

class Character:
	'''setup common characteristics of movable characters 
	---> player, npc, pathfinder characters etc'''
	def __init__(self,x, y, vel, l1,l2,r1,r2,d1,d2,u1,u2, width=15, height=19):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self._vel = vel #non-changing reference
		self.vel = vel
		self.walk_count = 0
		self.hitbox = (self.x, self.y, self.width, self.height)
		self.walk_left = [pygame.image.load(f'sprites/{l1}').convert_alpha(), pygame.image.load(f'sprites/{l2}').convert_alpha()]
		self.walk_right = [pygame.image.load(f'sprites/{r1}').convert_alpha(), pygame.image.load(f'sprites/{r2}').convert_alpha()]
		self.walk_down = [pygame.image.load(f'sprites/{d1}').convert_alpha(), pygame.image.load(f'sprites/{d2}').convert_alpha()]
		self.walk_up = [pygame.image.load(f'sprites/{u1}').convert_alpha(), pygame.image.load(f'sprites/{u2}').convert_alpha()]
		self.hit_slow = False #slowed movement area: grass/water

	def walk_animation(self, direction, win):
		if not self.hit_slow:
			win.blit(direction[self.walk_count//2], (self.x,self.y))
		else: #we are in grass/water
			 #chop off bottom of player
			win.blit(direction[self.walk_count//2], (self.x,self.y), (0,0,SnaptoGrid.snap(self.width),self.height-self.height//4))

		self.walk_count += 1

	def stand_sprite(self, direction, win):
		if not self.hit_slow:
				win.blit(direction, (self.x,self.y))
		else:
				win.blit(direction, (self.x,self.y), (0,0,SnaptoGrid.snap(self.width),self.height-self.height//4))

class Player(Character):
	def __init__(self,xy=(50,70)):
		super().__init__(xy[0],xy[1], 10, 'player/ash_left2.png','player/ash_left3.png','player/ash_right2.png','player/ash_right3.png','player/ash_down2.png', 'player/ash_down3.png', 'player/ash_up2.png', 'player/ash_up3.png')
		self.stand_left = pygame.image.load('sprites/player/ash_left1.png').convert_alpha()
		self.stand_right = pygame.image.load('sprites/player/ash_right1.png').convert_alpha()
		self.stand_up = pygame.image.load('sprites/player/ash_up1.png').convert_alpha()
		self.stand_down = pygame.image.load('sprites/player/ash_down1.png').convert_alpha()
		self.bike_left = [pygame.image.load('sprites/player/bike_left2.png').convert_alpha(),pygame.image.load('sprites/player/bike_left3.png').convert_alpha()]
		self.bike_right = [pygame.image.load('sprites/player/bike_right2.png').convert_alpha(),pygame.image.load('sprites/player/bike_right3.png').convert_alpha()]
		self.bike_up = [pygame.image.load('sprites/player/bike_up2.png').convert_alpha(), pygame.image.load('sprites/player/bike_up3.png').convert_alpha()]
		self.bike_down = [pygame.image.load('sprites/player/bike_down2.png').convert_alpha(), pygame.image.load('sprites/player/bike_down3.png').convert_alpha()]
		self.stand_left_bike = pygame.image.load('sprites/player/bike_left1.png').convert_alpha()
		self.stand_right_bike = pygame.image.load('sprites/player/bike_right1.png').convert_alpha()
		self.stand_up_bike = pygame.image.load('sprites/player/bike_up1.png').convert_alpha()
		self.stand_down_bike = pygame.image.load('sprites/player/bike_down1.png').convert_alpha()
		self.left = False
		self.right = False
		self.up = False
		self.down = True
		self.standing = True
		self.bike = False

	#draw ash onto the screen
	#animate directions
	def draw(self, win):
		if self.walk_count + 1 > 4:
			self.walk_count = 0
		if not self.standing:
			if self.right:
				if self.bike:
					self.walk_animation(self.bike_right, win)
				else: self.walk_animation(self.walk_right, win)
			elif self.left:
				if self.bike:
					self.walk_animation(self.bike_left, win)
				else: self.walk_animation(self.walk_left, win)
			elif self.up:
				if self.bike:
					self.walk_animation(self.bike_up, win)
				else: self.walk_animation(self.walk_up, win)
			elif self.down:
				if self.bike:
					self.walk_animation(self.bike_down, win)
				else: self.walk_animation(self.walk_down, win)
		else:
			if self.right:
				if self.bike:
					self.stand_sprite(self.stand_right_bike,win)
				else: self.stand_sprite(self.stand_right,win)
			elif self.left:
				if self.bike:
					self.stand_sprite(self.stand_left_bike,win)
				else: self.stand_sprite(self.stand_left,win)
			elif self.up:
				if self.bike:
					self.stand_sprite(self.stand_up_bike,win)
				else: self.stand_sprite(self.stand_up,win)
			elif self.down:	
				if self.bike:
					self.stand_sprite(self.stand_down_bike,win)
				else: self.stand_sprite(self.stand_down,win)

	def move(self, collision_zone, movement_cost_area):
		keys = pygame.key.get_pressed()

		#simple collision detection:
		#check if player (x,y) is in the set of object coordinates
		#given player dimensions (w=15,h=19) setting +/-10 (1 square) works ok
		bounds = (SnaptoGrid.snap(self.x),SnaptoGrid.snap(self.y+10))
		hit_wall = True if bounds in collision_zone else False
		self.hit_slow = True if bounds in movement_cost_area else False

		if self.hit_slow:
			#slow movement speed
				slow_speed = self._vel//2
				self.vel = slow_speed
		else:
			self.vel = self._vel
			#we must re-snap to grid as (x,y) no longer to nearest 10
			self.snap()

		if not hit_wall:
			if keys[pygame.K_LEFT]:
				self.x -= self.vel
				self.left = True
				self.right = False
				self.up = False
				self.down = False
				self.standing = False
				self.direction = 'L'
			elif keys[pygame.K_RIGHT]:
				self.x += self.vel
				self.left = False
				self.right = True
				self.up = False
				self.down = False
				self.standing = False
				self.direction = 'R'
			elif keys[pygame.K_UP]:
				self.y -= self.vel
				self.left = False
				self.right = False
				self.up = True
				self.down = False
				self.standing = False
				self.direction = 'U'
			elif keys[pygame.K_DOWN]:
				self.y += self.vel
				self.left = False
				self.right = False
				self.up = False
				self.down = True
				self.standing = False
				self.direction = 'D'
			else:
				self.standing = True
				self.walk_count = 0
		else: #collision
			if self.left: self.x += self.vel
			elif self.right: self.x -= self.vel
			elif self.up: self.y += self.vel
			elif self.down: self.y -= self.vel

		#prevent movement beyond the screen
		if self.x > config.window_width-config.grid_spacing:
			self.x -= self.vel
		elif self.x < 0:
			self.x += self.vel
		elif self.y < 0:
			self.y += self.vel
		elif self.y > config.window_height-self.height:
			self.y -= self.vel

	def snap(self):
		'''snap player x,y to grid'''
		self.x, self.y = SnaptoGrid.snap(self.x), SnaptoGrid.snap(self.y)


class Npc(Character):
	'''Npc character moves back and forth between specific coordinates'''
	def __init__(self, x, y, end):
		super().__init__(x,y,10,'player2/left2.png','player2/left3.png','player2/right2.png','player2/right3.png','player2/down2.png', 'player2/down3.png', 'player2/up2.png', 'player2/up3.png')
		self.end = end
		self.path = (self.x, self.end)
		
	def draw(self, win):
		self.move()
		if self.walk_count + 1 > 4:
			self.walk_count = 0
		if self.vel > 0:
			self.walk_animation(self.walk_right, win)
		else:
			self.walk_animation(self.walk_left, win)

	def move(self):
		if self.vel > 0: #moving right
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1 #switch direction
				self.walk_count = 0
		else: #moving left
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.walk_count = 0

# print(Player.__mro__) 
# print(Character.__doc__)