import random

class Dna():

    senses = []
    actuators = []

    def __init__(self, senses, actuators):
        self.senses = senses
        self.actuators = actuators

    def createNewDna(self):

        new_dna = []

        # decide length
        length = random.randrange(10, 50)

        for t in range(length):

            # pick sense
            s = random.randint(len(self.senses))

            # pick actuator
            a = random.randint(len(self.actuators))

            new_dna.append([s, s.get_random_trigger, a, a.get_random_action])

        return new_dna