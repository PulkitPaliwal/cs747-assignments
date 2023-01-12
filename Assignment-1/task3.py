"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the AlgorithmManyArms class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)
"""

from optparse import Values
from secrets import choice
import numpy as np

# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE

class AlgorithmManyArms:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        # Horizon is same as number of arms
        # START EDITING HERE
        # You can add any other variables you need here
        self.horizon = horizon
        self.values = np.zeros(self.num_arms)
        self.counts = np.zeros(self.num_arms) 
        self.main_count = 0
        self.prev_pull = np.random.randint(self.num_arms)
        self.prev_result = 0
        self.arms_to_be_pulled = []
        for i in range(num_arms):
            self.arms_to_be_pulled.append(i)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if(self.prev_result == 1):
            return self.prev_pull
        elif(np.max(self.values)>0.99):
            return np.argmax(self.values)
        else:
            self.arms_to_be_pulled = np.delete(self.arms_to_be_pulled, np.where(self.arms_to_be_pulled == self.prev_pull))
            self.prev_pull = np.random.choice(self.arms_to_be_pulled)
            return self.prev_pull
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        self.prev_result = reward
        # END EDITING HERE
