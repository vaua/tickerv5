import random


''' What the heck is even a concept? Somthing that appears in the world? I don't know...
    I think I tried to enumerate all the different features of the world, but it's not easy...

    Concepts, triggers and actions must hang together. Concepts and DNA must hand together.
    Concepts and world must hang together. Are concepts even necessary?

    But let's even get further away from that. Let's say DNA is directly belonging to the world, i.e. the world 
    creates and interprets DNA, through senses. How would that work? 

    Let's say - when randomly creating:
    GetRandomDna:
      sense = GetRandomSense
      trigger = sense.getRandomTrigger
      action = sense.getRandomAction <= from what??? From pool of all actions? From the concept (is this where it came from?)
      
      Cause seing something could lead to many actions. See bit - give birth. See bit - move. See bit - eat. How do we pick an appropriate,
      random action thus basically making the cell of that type? Have I considered this before??

      I guess I paired senses and actuators strongly before. Maybe OK to do so even now. Initially at least. And that would be a concept - a combination of sense and act?

      Ok. Starting to remember a little bit about concepts now. 
      Each concept will have a value for each individual. This is all there is - nothing else. This is the status of the world.
      Then, furthermore, each sense will have one or more concepts as input, and each actuator will have one or more concepts as output.

      So for the very simple case, experiment one. What concepts are there?
      - position - 1D Geometry. Expressed through value - position - that each entity has. There will be one sense operating on this concept,
        1Dvision. It will check the value of this parametar in other entities, to create a representation for the animal (trigger).
        There will be two actuators operating on this - movement and eating. Depending on their value it will alter the position (at times).
        These actuators will involve another concept as well, energy.

      - energy - Expressed through value - energy - which entity has. There will be no sense (initially) operating on this concept. There will be an 
        action operating on this concept - eating. Eating will cost energy if triggerred (but what will trigger it? It has to have a sense that triggers it!)

'''
class Concept:
    def initiate():
        pass

    def create_random_dna_contribution():
        pass

    def create_random_state():
        pass




class OneDSpaceConcept(Concept):
    
    def __init__(self, max_size):
        self.max_size = max_size
        
    def create_random_state(self):
        return random.randrange(self.max_size)

    def getLeft(self, position):
        if position == 0: 
            return self.max_size - 1
        
        return position - 1

    def getRight(self, position):
        if position == self.max_size - 1: 
            return 0
        
        return position + 1


class EnergyConcept(Concept):

    def __init__(self, maxEnergyForNewBeing):
        self.maxEnergyForNewBeing = maxEnergyForNewBeing

    def create_random_dna_contribution(self):
        return 0

    def create_random_state(self):
        return random.randrange(self.maxEnergyForNewBeing)

class AgeConcept(Concept):

    def __init__(self):
        self.age = 0

    def create_random_dna_contribution(self):
        return []

    def create_random_state(self):
        return self.age

    def getOldestAnimals(self, amount, world):

        oldestAnimals = []
        for entity in world.population:
            for pos in range(amount):
                if pos >= len(oldestAnimals):
                    oldestAnimals.append(entity)
                    break
                elif oldestAnimals[pos][0][world.AGE] < entity[0][world.AGE]:
                    oldestAnimals.insert(pos, entity)
                    break

        return oldestAnimals[:10]
