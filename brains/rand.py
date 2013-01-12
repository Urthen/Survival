from random import random, randrange

from base import Brain
from game.util import DIRECTION

class RandomBrain(Brain):
	
	def __init__(self):
		super(RandomBrain, self).__init__()
		self.redirect()

	def redirect(self):
		self.direction = DIRECTION.keys()[randrange(len(DIRECTION))]

	def iterate(self, state):	
		if random() < 0.05:
			self.redirect()

		if state.energy > state.birth_energy and random() < 0.1:
			return [('birth', 1)]

		if state.energy < state.max_energy:
			for direction in DIRECTION.keys():
				contents = state.map.at(*DIRECTION[direction]).contents
				if len(contents) > 0:
					if contents[0].description == "plant":
						return [('eat', contents[0])]

		attempts = 0

		while not (state.map.at(*DIRECTION[self.direction]).passable(state)) and attempts < 6:
			self.redirect()
			attempts += 1 #prevent infinite loops, I guess.

		return [('move', self.direction)]