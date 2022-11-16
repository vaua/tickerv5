import imp.concepts
import imp.senses
from ipycanvas import Canvas, hold_canvas
import copy


class World:

    def __init__(self, initial_population, replenish_level):
        # Initialize the world
        # First, read all concepts

        # Config vars
        self.population_size = initial_population
        self.replenish_level = replenish_level  

        self.concepts = []
        self.senses = []

        self.world_size = 1200
        self.concepts.append(imp.concepts.OneDSpaceConcept(self.world_size))
        self.POSITION = 0

        self.max_energy = 100
        self.concepts.append(imp.concepts.EnergyConcept(self.max_energy))
        self.ENERGY = 1

        self.concepts.append(imp.concepts.AgeConcept())
        self.AGE = 2

        self.senses.append(imp.senses.OneDVisionNoOrientationOnePixelRange())
        self.VISION = 0

        self.mutation_rate = 50
    
        self.population = []

        # stats
        self.stats_tick = 0
        self.eaten_animals = []
        self.chosen_dna = []#[[[0, 0], [0, 0], [4, 0], [1, 3], [6, 2], [7, 2], [3, 2], [2, 2], [1, 3], [5, 0]]]
        self.chosen_energy = 0
        self.chosen_seen_trigger = 0
        self.chosen_chosen_action = 0

        # drawing 
        self.draw_offset = 50
        self.draw_height = 200
        self.draw_width = 1000
        self.canvas = Canvas(width=self.draw_width, height=self.draw_height)
        self.draw_factor = (self.draw_width - (2 * self.draw_offset)) / self.world_size
        self.color_scheme = ["red", "blue", "orange", "green"]
        self.canvas

        ## Create initial random population
        self.create_inital_state(self.population_size)

    ## End of init



    # Adds an entity to World Status (i.e. population)
    def add_entity(self, concept_values, dna):
        new_entity = []
        new_entity.append(concept_values)
        new_entity.append(dna)
        self.population.append(new_entity)
        
    # Removes an entity from World Status
    def remove_entity(self, entity):
        self.population.remove(entity)

    def create_inital_state(self, entity_number):
        
        # Create population consisting of random individuals
        for i in range(entity_number):
            concept_values = []
            dna = []

            for sense in self.senses:

                sense_dna = []
                # Go over all concepts and get random inital values
                # For each concept, some random genes are created by each sense

                for concept in self.concepts:
                    concept_values.append(concept.create_random_state())

                    for gene in sense.create_random_dna_contribution():
                        sense_dna.append(gene);

                dna.append(sense_dna)

            self.population.append([concept_values, dna])

    def mutate_dna(self, dna):
        
        mutated_dna = []
        for i, sense in enumerate(self.senses):
            mutated_dna.append(sense.mutate_dna(dna[i], self.mutation_rate))

        return mutated_dna

    
    def tick(self):
        # trigger / action process
        sense_action_list = []

        # Initialize the list array with a action list for each sense
        for sense in self.senses:
            sense_action_list.append([])

        for entity in self.population:
            # Prepare each sense input that is relevant for indivudual - trigger
            for index, sense in enumerate(self.senses):
                trigger = sense.get_trigger_value(entity, self)
                #print("Enitity: ", enti, " trigger: ", trigger)

                sense_dna = entity[1][index]
                action = sense.get_sense_response_to_trigger(trigger, sense_dna)
                sense_action_list[index].append([entity, action])
            if entity[1] == self.chosen_dna:
                print("Found dodo")
                self.chosen_energy = entity[0][self.ENERGY]

        # execute senses and actions

        for index, sense in enumerate(self.senses):
            for action in sense_action_list[index]:
                if action[0][1] == self.chosen_dna:
                    print("Dodo again, chosen action is ", action[1])
                sense.execute_action(action, self)


        # Cost of living / Execute energy concept
        dead_entities = []
        for entity in self.population:
            ## Cost of living is one energy unit.
            entity[0][self.ENERGY] -= 1

            if entity[0][self.ENERGY] < 0:
                # Entity is dead. 
                dead_entities.append(entity)

        for dead_entity in dead_entities:
            self.remove_entity(dead_entity)

        # Execute age concept for all survivors
        for entity in self.population:
            entity[0][self.AGE] += 1

        # measure
        ## Get oldest animals
        oldies = self.concepts[self.AGE].getOldestAnimals(10, self)
        score = "Tick: " + str(self.stats_tick) + "  "
        for index, entity in enumerate(oldies):
            score += str(index) + ": " + str(entity[0][self.AGE]) + ","
            
        print("\r", score, end = '')


        # draw
        with hold_canvas():
            # Clear the old animation step
            self.canvas.clear()
            self.canvas.stroke_style = "red"
            self.canvas.stroke_line(self.draw_offset, self.draw_height - self.draw_offset, self.draw_width - self.draw_offset, self.draw_height - self.draw_offset)

            factor = 1
            #for entity in self.population:
            for entity, action in sense_action_list[0]:
                if entity[1] == self.chosen_dna:
                    factor = 5
                    print("Energy before: ", self.chosen_energy, ", energy now: ", entity[0][self.ENERGY])
                else:
                    factor = 1
                self.canvas.fill_style = "black" if action == [] else self.color_scheme[action[0]]
                if self.canvas.fill_style == "orange" and entity[1] in self.eaten_animals:
                    if (entity[1] == self.chosen_dna):
                        print("Dodo is having a tough time!")
                    self.canvas.fill_style = "pink"
                self.canvas.fill_rect(self.draw_offset + (entity[0][self.POSITION] * self.draw_factor), self.draw_height - (self.draw_offset + entity[0][self.ENERGY]), 3 * factor, 3 * factor)


        # replenish if needed
        if (len(self.population) < self.replenish_level):
            ## Time to replenish
            ## There will probably be some variants. But let's say we copy the top 10 and randomize the rest for this one?
            
            #Also, check how many to copy. Sometimes oldies will hold more than peeps to replenish
            to_replenish = self.population_size - len(self.population)
            if to_replenish < len(oldies):
                oldies_to_rep = oldies[:to_replenish]
            else:
                oldies_to_rep = oldies

            ## First copy the top
            for old in oldies_to_rep:
                new = copy.deepcopy(old)
                new[0][self.AGE] = 0
                new[0][self.POSITION] = self.concepts[self.POSITION].create_random_state()
                new[0][self.ENERGY] = self.concepts[self.ENERGY].create_random_state()
                self.add_entity(new[0], new[1])

            ## Add some mutated ones
            for old in oldies_to_rep:
                new = copy.deepcopy(old)
                new[0][self.AGE] = 0
                new[0][self.POSITION] = self.concepts[self.POSITION].create_random_state()
                new[0][self.ENERGY] = self.concepts[self.ENERGY].create_random_state()
                mutated_dna = self.mutate_dna(new[1])
                self.add_entity(new[0], new[1])


            ## Now add remainder random
            if (len(self.population) < self.population_size):
                self.create_inital_state(self.population_size - len(self.population))
        
        # adjust status
        self.stats_tick += 1
        self.eaten_animals = []
        

        #repeat
