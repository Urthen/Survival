from random import random, randrange

from world import Cell, Actor

class Plant(Actor):
	DESCRIPTION = "plant"
	SYMBOL = "P"
	COLOR = "BLACK"

class Forest(Cell):
	DESCRIPTION = "forest"
	COLOR = "GREEN"

	def __init__(self, world, x, y, spawn = False):
		super(Forest, self).__init__(world, x, y)
		if spawn and world.map(x, y).passable(1):
			world.spawn(Plant, x, y)

def generate_at_random(world, num = 20):
	for i in range(0, num):
		x = randrange(0, world.WIDTH)
		y = randrange(0, world.HEIGHT)

		for xd in range(-2, 3):
			for yd in range(-2, 3):
				if random() < 0.75:
					world.replace(x + xd, y + yd, Forest, spawn = (random() < 0.5))
