from random import random, randrange

from world import Actor
from state import SelfState
from brains.base import DIRECTION

class Animal(Actor):
	DESCRIPTION = "animal"

	def __init__(self, world, x, y, brain):
		super(Animal, self).__init__(world, x, y)
		self.brain = brain
		self.max_health = 100
		self.max_energy = 200
		self.energy = 100
		self.health = 100
		self.speed = 1
		self.eyesight = 10

		self.ACTIONS = {
			"move": self.handleMove
		}

	def iterate(self):
		state = SelfState(self)
		response = self.brain.iterate(state)

		if response is None:
			return

		self.moves = 0

		for action, value in response:
			if action in self.ACTIONS:
				self.ACTIONS[action](value)

	def handleMove(self, move):
		self.moves += 1
		if self.moves > self.speed:
			print "Attempted to move too far."
			return

		if move in DIRECTION:
			tx, ty = self.world.bound(*[x + y for x, y in zip([self.x, self.y], DIRECTION[move])])
			if self.world.map(tx, ty).passable(self.size):
				self.move(tx, ty)
		else:
			print "{0} is not a valid direction, ignoring move.".format(move)
