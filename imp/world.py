import imp.concepts
import copy, random
import time
from ipycanvas import Canvas, hold_canvas


class World:

    def __init__(self, initial_population, replenish_level):
        # Initialize the world
        # First, read all concepts

        # Config vars
        self.population_size = initial_population
        self.replenish_level = replenish_level  
        self.cost_of_living = 1

        self.concepts = []

        self.world_size = 1200
        self.position = imp.concepts.OneDSpaceConcept(0, self.world_size)
        self.concepts.append(self.position)
        self.POSITION = 0

        self.max_energy = 500
        self.energy = imp.concepts.EnergyConcept(1, self.max_energy)
        self.concepts.append(self.energy)
        self.ENERGY = 1

        self.world = imp.concepts.WorldConcept(2, self)
        self.concepts.append(self.world)
        self.WORLD = 2

        self.VISION = 0

        self.INTERNAL = 1

        self.mutation_rate = 50

        # Sun, a peculiar thing that is a part of the world
        self.sun_position = random.randrange(self.world_size)
        self.sun_size = 300
        self.sun_benefit = 3
    
        self.population = []
        self.entities_to_add = []


        # stats
        self.stats_tick = 0
        self.eaten_animals = []
        self.chosen_dna = [[[6, 1], [7, 0], [4, 1], [6, 0], [1, 0], [6, 2], [5, 3], [1, 2]], [[3, 1], [3, 2], [3, 5], [3, 0], [3, 0], [5, 7], [7, 0], [2, 6]]]
        self.chosen_energy = 0
        self.chosen_seen_trigger = 0
        self.chosen_chosen_action = 0
        self.restart_ticks = []

        # drawing 
        self.draw_offset = 50
        self.draw_height = 800
        self.draw_width = 1000
        self.canvas = Canvas(width=self.draw_width, height=self.draw_height)
        self.draw_factor = (self.draw_width - (2 * self.draw_offset)) / self.world_size
        self.color_scheme = ["red", "blue", "orange", "green"]
        self.canvas.width = 1000
        self.canvas.height = 1000

        ## Create initial random population
        #self.create_inital_state(self.population_size)

    ## End of init


    # Adds an entity to World Status (i.e. population)
    def add_entity(self, entity):
        self.population.append(entity)
        
    # Removes an entity from World Status
    def remove_entity(self, entity):
        self.population.remove(entity)

    def create_entity(self, dna, random = False):
        entity= [[], []]
        value = 0 if random == False else None

        for concept in self.concepts:
            concept.append_value(entity, value)
            concept.append_concept_dna(entity, dna)

        return entity

    def create_inital_state(self, entity_number):
        
        # Create population consisting of random individuals
        for i in range(entity_number):
            self.population.append(self.create_entity(None, True))


    def in_sun(self, entity):
        entity_position = self.position.get_value(entity)
        if ((entity_position < self.sun_size) and (self.sun_position > self.sun_size)):
            entity_position += self.world_size
        if ((entity_position > self.sun_position) and (entity_position < self.sun_position + self.sun_size)):
            #print("Animal in position", entity[0][self.POSITION], " in sun!")
            return True
        else:
            return False

    def get_entities_in_sun(self):

        entities_in_sun = []
        reminder = self.sun_position + self.sun_size - self.world_size

        for pos in range(self.sun_position, (self.sun_position + self.sun_size) if reminder < 0 else self.world_size):
            for entity in self.position.get_entities_in_position(pos):
                entities_in_sun.append(entity)

        if reminder > 0:
            for pos in range(0, reminder):
                for entity in self.position.get_entities_in_position(pos):
                    entities_in_sun.append(entity)

        return entities_in_sun
    

    
    def check_population_for_duplicates(self):
        for entity in self.population:
            if entity == self.chosen_dna:
                print("Chosen one when duplicating: ", entity)
            if self.population.count(entity) > 1:
                print("Whoa! Entity is multiple! ", entity)
    


    
    def tick(self):
        # trigger / action process
        tick_start_time = time.time()

        action_list = []
        self.entities_to_add = []

        for entity in self.population:
            # Go over all concepts. For each concept
            # Calculate trigger for each sense
            # Look up trigger in dna and get actions
            # build a list of actions to perfrom in the world

            for concept in self.concepts:
                #print("Appending actions for concept ", concept)
                actions = concept.get_actions(entity)
                if len(actions) > 0:
                    action_list.append([entity, concept.get_actions(entity)])
                    
        action_list_done_time = time.time()
        get_action_list_time = (action_list_done_time - tick_start_time)

        for entity, action_array in action_list:
            #entity = entity_actions[0]
            #action_array = entity_actions[1]
            #print("Entity: ", self.world.get_entity_id(entity), " action: ", action_array)
            for action_instance in action_array:
                #print("Action t: ", action_instance)
                #for t in action_instance:
                #    print("In array: ", t)
                sense = action_instance[0]
                actions = action_instance[1]
                sense.execute_action(entity, actions, self)

        action_execution_done = time.time()
        action_execution_time = (action_execution_done - action_list_done_time)

        ## Check population for duplicates
        #self.check_population_for_duplicates()


        # Sun and extra energy
        #for entity in self.population:
        #    if self.in_sun(entity):
        #        self.energy.add_value(entity, self.sun_benefit)
        
        for entity in self.get_entities_in_sun():
            self.energy.add_value(entity, self.sun_benefit)
        
        self.sun_position += 5
        if (self.sun_position > self.world_size):
            self.sun_position = 0


        # Cost of living / Execute energy concept
        dead_entities = []
        for entity in self.population:
            ## Cost of living is one energy unit.
            self.energy.add_value(entity, -self.cost_of_living)

            if self.energy.get_value(entity) < 0:
                # Entity is dead. 
                dead_entities.append(entity)

        for dead_entity in dead_entities:
            self.remove_entity(dead_entity)


        # Execute age concept for all survivors
        for entity in self.population:
            self.world.increase_age(entity)


        ## Add new born entities
        #print("Adding ", len(self.entities_to_add), " newborn entities.")
        for entity in self.entities_to_add:
            if (self.population.count(entity) > 0):
                print ("STOP: entity already exists!!!")
            self.add_entity(entity)


        # measure
        ## Get oldest animals
        oldies = self.world.get_oldest_animals(10)
        score = "Tick: " + str(self.stats_tick) #+ "  "
        #for index, entity in enumerate(oldies):
        #    score += str(index) + ": " + str(entity[0][self.WORLD][1]) + ","
            
        print("\r", score, end = '')

        population_shaping_done = time.time()
        population_shaping_time = (population_shaping_done - action_list_done_time)

        # draw
        with hold_canvas():
            # Clear the old animation step
            self.canvas.clear()
            self.canvas.stroke_style = "red"
            self.canvas.stroke_line(self.draw_offset, self.draw_height - self.draw_offset, self.draw_width - self.draw_offset, self.draw_height - self.draw_offset)

            factor = 1
            for entity, action_array in action_list:
                #if entity[1] == self.chosen_dna:
                #    factor = 5
                #    print("Energy before: ", self.chosen_energy, ", energy now: ", self.energy.getValue(entity))
                #else:
                #    factor = 1
                
                ## Get actions for position (first sense)
                ## Action array consists of: [sense, actions]
                for action in action_array:
                    if action[0] == self.position.senses[0]:
                        #print("Sense should be position: ", action[0])
                        #print("Found following actions for position sense: ", action[1])
                        self.canvas.fill_style = "black" if action[1] == [] else self.color_scheme[action[1][0]]
                        if self.canvas.fill_style == "orange" and entity[1] in self.eaten_animals:
                            if (entity[1] == self.chosen_dna):
                                print("Dodo is having a tough time!")
                            self.canvas.fill_style = "pink"
                        self.canvas.fill_rect(self.draw_offset + (self.position.get_value(entity) * self.draw_factor), self.draw_height - (self.draw_offset + self.energy.get_value(entity)), 3 * factor, 3 * factor)

            self.canvas.fill_style = "yellow"
            self.canvas.fill_rect(self.sun_position * self.draw_factor + self.draw_offset, self.draw_height, self.sun_size * self.draw_factor, -50)
            if (self.sun_position > self.world_size - self.sun_size):
                self.canvas.fill_rect(self.draw_offset, self.draw_height, (self.sun_size - (self.world_size - self.sun_position)) * self.draw_factor, -50)



        drawing_done = time.time()
        drawing_time = (drawing_done - population_shaping_done)
        

        # replenish if needed
        if (len(self.population) < self.replenish_level):
            ## Time to replenish
            ## There will probably be some variants. But let's say we copy the top 10 and randomize the rest for this one?
            
            self.restart_ticks.append(self.stats_tick)
            #Also, check how many to copy. Sometimes oldies will hold more than peeps to replenish
            to_replenish = self.population_size - len(self.population)
            if to_replenish < len(oldies):
                oldies_to_rep = oldies[:to_replenish]
            else:
                oldies_to_rep = oldies

            ## First copy the top
            for old in oldies_to_rep:
                dna = copy.deepcopy(old[1])
                entity = self.create_entity(dna, True)
                self.add_entity(entity)

            ## Add some mutated ones
            #for old in oldies_to_rep:
            #    dna = copy.deepcopy(old[1])
            #    entity[1] = self.mutate_dna(entity)
            #    entity = self.create_entity(True)
                
            #   self.add_entity(entity)

            ## Now add remainder random
            if (len(self.population) < self.population_size):
                self.create_inital_state(self.population_size - len(self.population))
        
        # adjust status
        self.stats_tick += 1
        self.eaten_animals = []
        
        replenishing_done = time.time()
        replenishing_time = (replenishing_done - drawing_done)

        tick_time = time.time() - tick_start_time
        print("Tick time: ", "{:.4f}".format(tick_time), ", action list: ", "{:.4f}".format(get_action_list_time), " execution: ", "{:.4f}".format(action_execution_time), " shaping: ", "{:.4f}".format(population_shaping_time), " drawing: ", "{:.4f}".format(drawing_time), " replenishin: ", "{:.4f}".format(replenishing_time), " Births: ", len(self.entities_to_add))
        #repeat
