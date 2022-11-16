import random

class Sense():

    '''This function returns a low and high value between which trigger is valid'''
    def get_valid_trigger_range(self):
        pass

    '''This function is called every time environment state should be translated into what specific sense on entity sees'''
    def get_trigger_value(self, entity, population):
        pass

    def get_random_trigger(self):
        pass

class OneDVisionNoOrientationOnePixelRange(Sense):

    def __init__(self):

        ## Constants
        self.cost_of_move = 2
        self.cost_of_eat = 3
        self.benefit_of_eating = 5
        self.hurt_of_eating = 6



        ## Trigger input consist of three bits - each bit indicates entity present left, center, right
        self.trigger_range = [0, 8]

        ## Output consists of four possible actions: go left, stay, eat, go right  ["red", "blue", "orange", "green"]
        self.actuator_range = [0, 4]

        self.max_number_of_genes_to_random_contribution = 10


    def create_random_dna_contribution(self):

        dna = []

        ## A DNA from a sense consists of a number of valid triggers, along with 
        amount_of_genes_to_create = random.randrange(self.max_number_of_genes_to_random_contribution)

        for gene in range(amount_of_genes_to_create):
            # Create a random trigger and random action pair
            trigger = random.randrange(self.trigger_range[0], self.trigger_range[1])
            action = random.randrange(self.actuator_range[0], self.actuator_range[1])
            dna.append([trigger, action])

        return dna

    def mutate_dna(self, dna, mutation_rate):
        for gene in dna:
            if (random.randint(0, 99) < mutation_rate):
                gene[0] += 1
                if gene[0] == self.trigger_range[1]:
                    gene[0] = self.trigger_range[0]
            if (random.randint(0, 99) < mutation_rate):
                gene[1] += 1
                if gene[1] == self.actuator_range[1]:
                    gene[1] = self.actuator_range[0]
        return dna


    def get_trigger_value(self, entity, world):
        
        ## This trigger will return a 3 bit value, based on population
        ## Leftmost bit: 1 if something to the left (in the range positions)
        ## Middle bit. 1 if something in the same position as I
        ## Right bit - if something is in the range on the right

        
        pos1, pos2, pos3 = [0, 0, 0]
        entity_position = entity[0][world.POSITION]

        ## Check if anybody to the left
        for p in world.population:
            #print("Checking ", p)
            if (p == entity):
                #print("Found me.")
                continue

            #print ("Checking ", p[0][world.POSITION], " against ",  world.concepts[world.POSITION].getLeft(entity_position))
            if p[0][world.POSITION] == world.concepts[world.POSITION].getLeft(entity_position):
                pos1 = 1
            #print ("Checking ", p[0][world.POSITION], " against ",  entity_position)
            if p[0][world.POSITION] == entity_position:
                pos2 = 1
            if p[0][world.POSITION] == world.concepts[world.POSITION].getRight(entity_position):
                pos3 = 1
        
        trigger = (pos1 * 4) + (pos2 * 2) + pos3

        
        return trigger

    # Check if the trigger, as generated by the world, will produce some action.
    def get_sense_response_to_trigger(self, trigger, dna):
        triggered_actions = []
        chosen_actions = []

        logging = 0

        for gene in dna:
            if trigger == gene[0]:
                ## Trigger matched!
                triggered_actions.append(gene[1])

        if triggered_actions == []:
            return []
        else:
            chosen_actions.append(max(set(triggered_actions), key = triggered_actions.count))
            return chosen_actions

    def execute_action(self, actionin, world):
        entity = actionin[0]
        actions = actionin[1]
        concept_values = entity[0]
        
        for action in actions:
            ## Now execute the action. And remeber: go left, stay, eat, go right
            ## 0 == left - set position to one to the left, take down energy.
            if action == 0:
                concept_values[world.POSITION] = world.concepts[world.POSITION].getLeft(concept_values[world.POSITION])
                concept_values[world.ENERGY] = concept_values[world.ENERGY] - self.cost_of_move
            elif action == 1:
                ## Nothing - we're just chilling
                continue
            elif action == 2:
                ## We're going to eat. Now - let's check if there is somebody else in the same position
                #if entity[1] == [[[0, 0], [0, 0], [4, 0], [1, 3], [6, 2], [7, 2], [3, 2], [2, 2], [1, 3], [5, 0]]]:
                #    print("I'm pepe, at position ", entity[0][0], " with energy: ", entity[0][1], " aiming to eat.")
                for e in world.population:
                    if e == entity: 
                        ## It is me...
                        continue
                    if e[0][world.POSITION] == entity[0][world.POSITION]:
                        # OK, now we have found an animal who we can eat.
                        ## Raise energy for the eater, and lower for the eatee.
                        concept_values[world.ENERGY] += self.benefit_of_eating
                        e[0][world.ENERGY] -= self.hurt_of_eating
                        world.eaten_animals.append(e[1])
                        #print("I'm at position ", entity[0][0], " and I'm eating ", e[0][0], " with energy ", e[0][1])
                        if entity[1] == world.chosen_dna:
                            print("I'm pepe, at position ", entity[0][0], " having eaten, now energy is ", entity[0][1])
                        if e[1] == world.chosen_dna:
                           print("I'm pepe, at position ", entity[0][0], " being eaten!!!, now energy is ", e[0][1])

            ## Goind right
            elif action == 3:
                concept_values[world.POSITION] = world.concepts[world.POSITION].getRight(concept_values[world.POSITION])
                concept_values[world.ENERGY] = concept_values[world.ENERGY] - self.cost_of_move
            else:
                print("Cardinal error - output outside of triger")

