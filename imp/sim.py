'''This is the main file of the simulation'''
from imp.actuators import OneDMotor
from imp.entity import Entity
from imp.senses import Vision
import world
import concepts
import senses
import actuators
import dna

## Before we start anything:
# world / environment should be initialised and all concepts registered
# Dna should be initialised and all senses and actuators registered

#Figure out how many we want to start with
START_ENTITIES = 1000
REPLENISH_PER_TURN = 10

senses = []
actuators = []

senses.append(Vision())
actuators.append(OneDMotor())

dna = dna.Dna(senses, actuators)


population = []

for i in range(START_ENTITIES):
    edna = dna.createNewDna()
    entity = Entity(edna)
    entity.append(concepts.getRandomSnapshot(entity))
    population.append(entity)
