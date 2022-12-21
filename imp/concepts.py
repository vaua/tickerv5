import random
import imp.senses


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

    def get_value(self, entity):
        return entity[0][self.id]

    def set_value(self, entity, value):
        entity[0][self.id] = value

    def add_value(self, entity, value):
        entity[0][self.id] += value

    def append_value(self, entity, value = None):
        if value == None:
            value = self.get_initial_value()
        entity[0].append(value)
        #print("Appended value ", value, " for concept ", self.id)
        # Verify that correct value
        if self.get_value(entity) != value:
            print("Error: The appended value {} does not correspond to read value {}", value, self.getValue(entity))

    def get_concept_dna(self, entity, sense):
        return entity[1][self.id][sense.id]

    def set_concept_dna(self, entity, sense, dna):
        entity[1][self.id][sense.id] = dna

    def append_concept_dna(self, entity, dna = None):
        if dna == None:
            dna = self.get_initial_dna()
        entity[1].append(dna)
        # Verify that correct value
        #for sense in self.senses:
        #    if self.get_concept_dna(entity, sense) != dna:
        #        print("Error: The appended dna {} does not correspond to read dna {}", dna, self.getConceptDna(entity))

    def get_initial_dna(self):
        dna = []
        for sense in self.senses:
            dna.append(sense.get_random_sense_dna())
        
        return dna

    def mutate_concept_dna(self, entity, mutation_rate):
        
        for sense in self.senses:
            sense_dna = self.get_concept_dna(entity, sense)
            if len(sense_dna) < 2:
                print("Short DNA found, ", sense_dna, " in entity ", entity[0][2][0], "\n")
            self.set_concept_dna(entity, sense, sense.mutate_dna(sense_dna, mutation_rate))

    def get_actions(self, entity):
        actions_array = []

        for sense in self.senses:
            trigger = sense.get_trigger_value(entity, self)
            #print("Trigger: ", trigger)
            actions = sense.get_sense_response_to_trigger(trigger, self.get_concept_dna(entity, sense))
            #if (len(actions) == 0): continue
            #print("Identified Actions: ", actions)
            actions_array.append([sense, actions])

        #print("Actions array: ", actions_array)
        return actions_array


class OneDSpaceConcept(Concept):
    
    def __init__(self, id, max_size):
        self.id = id
        self.max_size = max_size
        self.positions = [[] for i in range(self.max_size)]
        self.senses = []
        self.senses.append(imp.senses.OneDVisionNoOrientationOnePixelRange(0))


        ### Trying now out a new idea, that concepts should own senses and actuators conected to them.
        ## Sense is pretty straight forward as concepts only affect one sense (true?). But even if
        ## There is more, they will all be connected to that one sense.
        ## But the available actions may have impact on several things and even on other animals.
        ## So - how to deal with that. For example - vision sense, which is part of OneDSpace context
        ## does its work based on where animals are in the OneD Space. But it will also be able to
        ## show other things - still the same tool? How about hearing it is also connected to 
        ## place in the room, but is quite different than vision. Is that then another sense in the space concept?
        ## Ok, that may hold!
        ## Then to the activators. They include moving - pretty given, where animals change their position, which
        ## is mostly what this concept guides. But then comes the tricky part - let's add animal looks
        ## to the mix. For this, I will need another container for description of it, so new concept
        ## But this new concept will need to be used by the vision (or it will need to superseed vision?)
        ## Or will they both be actually active at the same time, new one being added?
        ## And then, actuators will be the same, the decision to move, or stay, or to eat. So it would make sense to just have
        ## It as a part of the same system.

        ## So with all said - how about the interface? Let's start with that - changes to concept values are only done through the
        ## Conecept itself, by sending in the appropriate entity, and either ask for a value or change (direct or relative)
        
    def get_initial_value(self):
        return random.randrange(self.max_size)

    def get_left(self, entity):
        position = self.get_value(entity)
        #print("Checked position it is {}", position)
        #print("Entity is: ", entity)
        if position == 0: 
            return self.max_size - 1
        
        return position - 1

    def get_right(self, entity):
        position = self.get_value(entity)
        if position == self.max_size - 1: 
            return 0
        
        return position + 1

    #def getPosition(self, entity):
    #    # Return first number in the concept values of the entity
    #    return entity[0][0]

    ## Copied from the 
    def append_value(self, entity, value = None):
        super().append_value(entity, value)
        self.positions[self.get_value(entity)].append(entity)

    def set_value(self, entity, position, new_entity = False):
        current_position = self.get_value(entity)
        #print("Moving position from ", current_position, " to ", position)
        # Remove current position from the position array
        if (new_entity == False):
           self.positions[current_position].remove(entity)
        # Add entity in the new position
        self.positions[position].append(entity)
        super().set_value(entity, position)

    def entity_exist_to_left(self, entity):
        position_left = self.get_left(entity)
        if len(self.positions[position_left]) > 0:
            return True

        return False
    
    def entity_exist_to_right(self, entity):
        position_right = self.get_right(entity)
        if len(self.positions[position_right]) > 0:
            return True

        return False

    def entity_exist_in_place(self, entity):
        position = self.get_value(entity)
        if len(self.positions[position]) > 1:
            return True

        return False

    def get_entities_in_position(self, position):
        return self.positions[position]

    def remove_entity(self, entity):
        position = self.get_value(entity)
        self.positions[position].remove(entity)


class EnergyConcept(Concept):

    def __init__(self, id, max_energy):
        self.id = id
        self.max_energy = max_energy
        self.senses = []
        self.senses.append(imp.senses.InternalEnergy(0))

    def get_initial_value(self):
        return random.randrange(self.max_energy)


class WorldConcept(Concept):

    # This should be the "world concept", keeping note of things that are external to the 
    # animal, but still tied to it, like age, number etc.
    # Energy, position etc could be considered this, but I don't know right now.

    def __init__(self, id, world):
        self.id = id
        self.age = 0
        self.generation = 0
        self.entity_id_counter = 0
        self.world = world
        self.senses = []

    def get_initial_value(self):
        self.entity_id_counter += 1
        return [self.entity_id_counter, self.age, self.generation, {}]

    def get_oldest_animals(self, amount):

        oldestAnimals = []
        for entity in self.world.population:
            for pos in range(amount):
                if pos >= len(oldestAnimals):
                    oldestAnimals.append(entity)
                    break
                elif oldestAnimals[pos][0][self.world.WORLD][1] < entity[0][self.world.WORLD][1]:
                    oldestAnimals.insert(pos, entity)
                    break

        return oldestAnimals[:amount]

    def get_highest_generation(self):
        oldest_generation = 0
        for entity in self.world.population:
            if self.get_generation(entity) > oldest_generation:
                oldest_generation = self.get_generation(entity)
        
        return oldest_generation
    
    def get_entities_with_generation(self, generation):
        entities = []
        for entity in self.world.population:
            if self.get_generation(entity) == generation:
                entities.append(entity)

        return entities

    def get_entity_id(self, entity):
        return self.get_value(entity)[0]

    def get_entity_age(self, entity):
        return self.get_value(entity)[1]

    def increase_age(self, entity):
        world_stat = self.get_value(entity)
        world_stat[1] += 1 # Increases age, which is stored as parameter 1 by 1
        self.set_value(entity, world_stat)

    def get_generation(self, entity):
        return self.get_value(entity)[2]

    def set_generation(self, entity, generation):
        world_stat = self.get_value(entity)
        world_stat[2] = generation # Increases age, which is stored as parameter 1 by 1
        self.set_value(entity, world_stat)

    def get_last_actions(self, entity, concept):
        #print("Fetching last action is ", self.get_value(entity)[2])
        if (concept in self.get_value(entity)[3]):
            return self.get_value(entity)[3][concept]
        else:
            return []

    def set_last_actions(self, entity, concept, actions):
        world_stat = self.get_value(entity)
        world_stat[3][concept] = actions
        #print("Setting Last action to: ", world_stat[2])
        self.set_value(entity, world_stat)

