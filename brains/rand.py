from random import random, randrange

from base import Brain, DIRECTION

class RandomBrain(Brain):
	
	def __init__(self):
		super(RandomBrain, self).__init__()
		self.redirect()

	def redirect(self):
		self.direction = DIRECTION.keys()[randrange(len(DIRECTION))]

	def iterate(self, state):	
		if random() > 0.95:
			self.redirect()

		attempts = 0

		while not (state.map.at(*DIRECTION[self.direction]).passable(state)) and attempts < 6:
			self.redirect()
			attempts += 1 #prevent infinite loops, I guess.
			
		return [('move', self.direction)]