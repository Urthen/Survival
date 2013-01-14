from random import random, randrange

from world import Actor
from state import SelfState
from util import DIRECTION

class Corpse(Actor):
	SYMBOL = "c"
	DESCRIPTION = "corpse"
	COLOR = "RED"
	SIZE = 0.4

	def __init__(self, world, x, y, meat):
		super(Corpse, self).__init__(world, x, y)
		self.meat = meat

	def iterate(self):
		super(Corpse, self).iterate()

		if self.age % 10 == 0:
			self.meat -= 1

		if self.meat <= 0:
			self.die()

class Animal(Actor):
	SYMBOL = "M"
	DESCRIPTION = "animal"
	COLOR = "MAGENTA"
	STYLE = "BRIGHT"
	SIZE = 0.5

	def __init__(self, world, x, y, brain):
		super(Animal, self).__init__(world, x, y)
		self.brain = brain
		self.max_health = 100
		self.max_energy = 200
		self.birth_energy = 120
		self.energy = 30
		self.health = 100
		self.speed = 1
		self.eyesight = 10

	def die(self):
		super(Animal, self).die()
		self.world.spawn(Corpse, self.x, self.y, int(self.max_energy / 50))

	def iterate(self):
		super(Animal, self).iterate()

		if self.age > 100:
			self.max_health -= 2
			self.max_energy -= 2
			self.health -= 2
			self.energy -= 1
		else:
			self.health += 1

		self.energy -= 1
		if self.energy <= 0:
			self.health -= 15
		elif self.energy > self.max_energy:
			self.energy = self.max_energy

		if self.health <= 0:
			self.die()
			return
		elif self.health > self.max_health:
			self.health = self.max_health

		state = SelfState(self)
		response = self.brain.iterate(state)

		if response is None:
			return

		self.moves = 0

		for action, value in response:
			if hasattr(self, "handle_" + action):
				getattr(self, "handle_" + action)(value)

	def handle_move(self, move):
		self.moves += 1
		if self.moves > self.speed:
			print "Attempted to move too far."
			return

		if move in DIRECTION:
			tx, ty = self.world.bound(*[x + y for x, y in zip([self.x, self.y], DIRECTION[move])])
			if self.world.map(tx, ty).passable(self.size):
				self.move(tx, ty)
				self.energy -= 1
		else:
			print "{0} is not a valid direction, ignoring move.".format(move)

	def handle_eat(self, target):
		if target.id in self.world.actors:
			self.world.actors[target.id].food -= 1
			self.energy += 4

	def handle_birth(self, amount):
		if self.energy >= self.birth_energy * amount:
			self.energy -= self.birth_energy * amount
			for i in range(amount):
				self.world.spawn(Animal, self.x, self.y, self.brain.__class__())