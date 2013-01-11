from colorama import Fore, Back
from state import ObjectState, CellState

class Actor(object):
	DESCRIPTION = "unknown"
	SYMBOL = '?'	
	COLOR = "WHITE"
	PRIORITY = 0

	def __init__(self, world, x, y):
		self.x = x
		self.y = y
		self.world = world
		self.size = 1

	def __cmp__(self, other):
		return cmp(self.PRIORITY, other.PRIORITY)

	def move(self, x, y):
		self.world.move(self, x, y)

	@property
	def state(self):
		return ObjectState(self)

	def iterate(self):
		pass

class Cell(object):
	DESCRIPTION = "barren"
	COLOR = "RESET"
	PASSABLE = True

	def __init__(self, world, x, y):
		self.x = x
		self.y = y
		self.world = world
		self.contents = []
		self.state = CellState(self)

	def add(self, obj):
		self.contents.append(obj)
		self.state = CellState(self)

	def remove(self, obj):
		self.contents.remove(obj)
		self.state = CellState(self)

	@property
	def capacity(self):
		return 1 - reduce(lambda x, y: x + y.size, self.contents, 0)

	def passable(self, size=0):
		return self.PASSABLE and self.capacity >= size

	@property
	def tile(self):
		if len(self.contents) == 0:
			return Fore.WHITE + getattr(Back, self.COLOR) + '.'
		else:
			return getattr(Fore, self.contents[0].COLOR) + getattr(Back, self.COLOR) + self.contents[0].SYMBOL

	def iterate(self):
		pass

	def replace(self, replacement, *args, **kwargs):
		self.world.replace(self.x, self.y, replacement, *args, **kwargs)

class World(object):
	WIDTH = 200
	HEIGHT = 40

	def __init__(self):
		self.actors = []
		self._map = [[Cell(self, x, y) for x in range(0, self.WIDTH)] for y in range(0, self.HEIGHT)]

	def __str__(self):
		return '\n'.join([''.join(map(lambda cell: cell.tile, row)) for row in self._map]) + Fore.RESET + Back.RESET

	def bound(self, x, y):
		if x < 0:
			x += self.WIDTH
		elif x >= self.WIDTH:
			x -= self.WIDTH

		if y < 0:
			y += self.HEIGHT
		elif y >= self.HEIGHT:
			y -= self.HEIGHT

		return x, y

	def relativePos(self, dest, source):
		x = dest.x - source.x
		y = dest.y - source.y
		if x < (0 - self.WIDTH) / 2:
			x += self.WIDTH
		elif x > self.WIDTH / 2:
			x -= self.WIDTH
		if y < (0 - self.HEIGHT) / 2:
			y += self.HEIGHT
		elif y > self.HEIGHT / 2:
			y -= self.HEIGHT

		return x, y

	@property
	def cells(self):
		return reduce(lambda x, y: x + y, self._map)

	def map(self, x, y):
		x, y = self.bound(x, y)
		return self._map[y][x]

	def surroundings(self, center, dist):
		surroundings = []
		actors = []
		for y in range(center.y - dist, center.y + dist + 1):
			row = []
			for x in range(center.x - dist, center.x + dist + 1):
				cell = self.map(x, y)
				row.append(cell.state)
				actors.extend([actor.state for actor in cell.contents])
			surroundings.append(row)
		return surroundings, actors

	def replace(self, x, y, replacement, *args, **kwargs):
		x, y = self.bound(x, y)
		contents = self._map[y][x].contents
		replaced = replacement(self, x, y, *args, **kwargs)
		replaced.contents = contents
		replaced.state = CellState(replaced)
		self._map[y][x] = replaced

	def spawn(self, actor, x, y, *args, **kwargs):
		x, y = self.bound(x, y)
		obj = actor(self, x, y, *args, **kwargs)
		self.actors.append(obj)
		self._map[y][x].add(obj)

	def move(self, actor, x, y):
		self._map[actor.y][actor.x].remove(actor)
		actor.x = x
		actor.y = y
		self._map[y][x].add(actor)

	def iterate(self):
		for thing in self.cells + self.actors:
			thing.iterate()
