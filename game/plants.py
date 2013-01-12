from random import random, randrange
from util import DIRECTION

from world import Cell, Actor
from state import MapState

class Plant(Actor):
	DESCRIPTION = "plant"
	SYMBOL = "P"
	COLOR = "BLACK"

	def __init__(self, world, x, y):
		super(Plant, self).__init__(world, x, y)
		self.food = 6

	def iterate(self):
		super(Plant, self).iterate()

		if self.age > randrange(50, 120) or self.food <= 0:
			self.die()
			return

class Forest(Cell):
	DESCRIPTION = "forest"
	COLOR = "GREEN"

	def __init__(self, world, x, y, spawn = False):
		super(Forest, self).__init__(world, x, y)
		if spawn and world.map(x, y).passable(1):
			world.spawn(Plant, x, y)

		self.growth=randrange(1, 40)

	def iterate(self):

		cells, actors = self.world.surroundings(self, 1)

		trees = len([1 for actor in actors if type(actor) == Plant])
		forest = len([1 for cell in reduce(lambda x, y: x + y, cells, []) if type(cell) == Forest])

		empty = True
		for actor in self.contents:
			if type(actor) == Plant:
				empty = False
				break

		if trees > 3 or (forest > 4 and trees > 1):
			self.growth += 1
		else:
			if empty:
				self.growth -= 1

		if self.growth > 40 and trees < 4 and trees > 1:
			if random() < 0.1 and self.world.map(self.x, self.y).passable(1):
				self.world.spawn(Plant, self.x, self.y)
				self.growth -= 40
		if not empty and (trees > 2 or forest > 5): 
			for direction in DIRECTION.values():
				target = self.world.map(self.x + direction[0], self.y + direction[1])
				if random() < 0.1 and type(target) is Cell:
					target.replace(Forest)


		if self.growth > 50:
			self.growth = 50

		if self. growth <= 0 and empty:
			self.replace(Cell)

def generate_at_random(world, num = 20):
	for i in range(0, num):
		x = randrange(0, world.WIDTH)
		y = randrange(0, world.HEIGHT)

		for xd in range(-2, 3):
			for yd in range(-2, 3):
				if random() < 0.75:
					world.replace(x + xd, y + yd, Forest, spawn = (random() < 0.5))
