import os, time
from random import randrange

from game.world import World
from game import plants
from game.animals import Animal
from brains.rand import RandomBrain

import cProfile

AUTO = True
PROFILE = False

def clear():
	os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

world = World();
for x in range(40):
	world.spawn(Animal, randrange(world.WIDTH), randrange(world.HEIGHT), RandomBrain())
plants.generate_at_random(world, 100)

x = ''
while True:
	print world
	if AUTO:		
		time.sleep(0.05)
	else:
		x = raw_input("press enter to continue, ctrl-c to quit")

	if PROFILE:
		clear()		
		cProfile.run("for i in range(1, 10): world.iterate()")
	else:
		world.iterate()
		clear()