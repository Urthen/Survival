import os, time
from random import randrange

from game.world import World
from game import plants
from game.animals import Animal
from brains.rand import RandomBrain

import cProfile

PLANTS = 50
ANIMALS = 40
PRECALC = 0
AUTO = True	
PROFILE = False

def clear():
	os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

world = World();

plants.generate_at_random(world, PLANTS)

if PRECALC > 0:
	print "Precalculating %i moves..." % PRECALC
	for x in range(PRECALC):
		world.iterate()

world.turn = 0

for x in range(ANIMALS):
	world.spawn(Animal, randrange(world.WIDTH), randrange(world.HEIGHT), RandomBrain())

x = ''
while True:
	print world
	print "Turn", world.turn, "Animals", len([actor for actor in world.actors.values() if actor.DESCRIPTION == "animal"])
	if AUTO:		
		pass #time.sleep(0.05)
	else:
		x = raw_input("press enter to continue, ctrl-c to quit")

	if PROFILE:
		clear()		
		cProfile.run("for i in range(10): world.iterate()")
	else:
		world.iterate()
		clear()