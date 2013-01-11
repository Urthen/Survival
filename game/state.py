import math

class MapState(object):
	TYPE = "MAP"

	def __init__(self, cells):
		self._offsx = int(math.ceil(len(cells[0]) / 2))
		self._offsy = int(math.ceil(len(cells) / 2))
		self._cells = cells

	def at(self, x, y):
		return self._cells[y + self._offsy][x + self._offsx] 


class ObjectState(object):
	TYPE = "OBJECT"

	def __init__(self, source):
		self.qualifiers = []
		self.x = source.x
		self.y = source.y
		self.description = source.DESCRIPTION

	def __repr__(self):
		return "{0} ({1}, {2})".format(self.description, self.x, self.y)

class CellState(ObjectState):
	TYPE = "CELL"

	def __init__(self, source):
		super(CellState, self).__init__(source)
		self.capacity = source.capacity
		self._passable = source.PASSABLE

	def passable(self, actor):
		return self.passable and self.capacity >= actor.size

class SelfState(ObjectState):
	TYPE = "SELF"

	def __init__(self, source):
		super(SelfState, self).__init__(source)
		surroundings, actors = source.world.surroundings(source, source.eyesight)
		self.map = MapState(surroundings)
		self.actors = {}
		for actor in actors:
			if actor.description in self.actors:
				self.actors[actor.description] = actor
			else:
				self.actors[actor.description] = [actor]

		self.health = source.health
		self.max_health = source.max_health
		self.max_energy = source.max_energy
		self.energy = source.energy
		self.speed = source.speed
		self.size = source.size
		self.eyesight = source.eyesight

	def __repr__(self):
		return "\n".join(["{0}: {1}".format(attr, getattr(self, attr.lower())) for attr in self.ATTRS_TO_COPY])