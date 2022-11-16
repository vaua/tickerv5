import random

class Actuator():

    '''This function returns a low and high value between which action is valid'''
    def get_valid_action_range(self):
        pass

    '''This function is called every time an action should be returned to the environment'''
    def get_action_value(self, entity, population):
        pass

    def get_random_action(self):
        pass


class OneDMotor(Actuator):

    def get_random_action(self):
        return random.randrange(self.get_valid_action_range)


