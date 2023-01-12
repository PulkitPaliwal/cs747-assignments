from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """
        self.oriented = False
        self.ANGULAR_THRESHOLD = 4
        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        # Replace with your implementation to determine actions to be taken
        action_steer = 0
        action_acc = 0
        if(self.oriented == False):
            pos_x = -state[0]
            pos_y = state[1]
            velocity = state[2]
            heading = state[3]
            desired_orientation =np.abs(180/np.pi * (np.arctan2(-pos_y,-350-pos_x)) - 180)
            if(desired_orientation - heading > self.ANGULAR_THRESHOLD):
                action_acc = 2
                action_steer = 2
            elif(desired_orientation - heading < self.ANGULAR_THRESHOLD):
                action_acc = 2
                action_steer = 0
        else:
            action_acc = 4
            action_steer = 1
        action = np.array([action_steer, action_acc])  

        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
            
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            self.oriented = False
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                pos_x = -state[0]
                pos_y = state[1]
                velocity = state[2]
                heading = state[3]
                desired_orientation =np.abs(180/np.pi * (np.arctan2(-pos_y,-350-pos_x)) - 180)

                if(np.abs(heading - desired_orientation) < self.ANGULAR_THRESHOLD):
                    self.oriented = True
                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """
        self.init_pose = [0,0]
        self.centers = [[0,0],[0,0],[0,0],[0,0]]
        self.oriented = False
        self.avoidance_quadrant = 0
        self.avoidance_center = [0,0]
        self.THRESHOLD_ANGLE = 3
        self.THRESHOLD_Y = 30
        self.OBSTACLE_THRESHOLD = 30
        super().__init__()
            
    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        pos_x = state[0]
        pos_y = state[1]
        velocity = state[2]
        heading = state[3]

        if(self.oriented):
            action_steer = 1
            action_acc = 4
        
        elif(np.abs(pos_y) < self.THRESHOLD_Y):
            action_acc = 2
            if heading < 180:
                action_steer = 0
            else:
                action_steer = 2
        
        elif(self.avoidance_quadrant == 1):
            if(np.abs(pos_x - self.avoidance_center[0]) > 50 + self.OBSTACLE_THRESHOLD or np.abs(pos_y) < np.abs(self.avoidance_center[1])):
                if(np.abs(heading - 270) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 270 and heading > 90:
                        action_steer = 2
                    else:
                        action_steer = 0
            else:
                if(np.abs(heading - 180) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 180:
                        action_steer = 2
                    else:
                        action_steer = 0
        
        elif(self.avoidance_quadrant == 2):
            if(np.abs(pos_x - self.avoidance_center[0]) > 50 + self.OBSTACLE_THRESHOLD or np.abs(pos_y) < np.abs(self.avoidance_center[1])):
                if(np.abs(heading - 270) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 270 and heading > 90:
                        action_steer = 2
                    else:
                        action_steer = 0
            
            else:
                if(np.abs(heading) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 180:
                        action_steer = 0
                    else:
                        action_steer = 2
            
        
        elif(self.avoidance_quadrant == 3):
            if(np.abs(pos_x - self.avoidance_center[0]) > 50 + self.OBSTACLE_THRESHOLD or np.abs(pos_y) < np.abs(self.avoidance_center[1])):
                if(np.abs(heading - 90) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 270 and heading > 90:
                        action_steer = 0
                    else:
                        action_steer = 2
            
            else:
                if(np.abs(heading) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 180:
                        action_steer = 0
                    else:
                        action_steer = 2
        
        elif(self.avoidance_quadrant == 4):
            if(np.abs(pos_x - self.avoidance_center[0]) > 50 + self.OBSTACLE_THRESHOLD or np.abs(pos_y) < np.abs(self.avoidance_center[1])):
                if(np.abs(heading - 90) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 270 and heading > 90:
                        action_steer = 0
                    else:
                        action_steer = 2
            else:
                if(np.abs(heading - 180) < self.THRESHOLD_ANGLE):
                    action_acc = 4
                    action_steer = 1
                else:
                    action_acc = 2
                    if heading < 180:
                        action_steer = 2
                    else:
                        action_steer = 0
        
        else:
            if(pos_y > 0):
                if(np.abs(heading - 270) < self.THRESHOLD_ANGLE):
                        action_acc = 4
                        action_steer = 1
                else:
                    action_acc = 2
                    if heading < 270 and heading > 90:
                        action_steer = 2
                    else:
                        action_steer = 0
            else:
                if(np.abs(heading - 90) < self.THRESHOLD_ANGLE):
                        action_acc = 4
                        action_steer = 1
                else:
                    action_acc = 2
                    if heading < 270 or heading > 90:
                        action_steer = 0
                    else:
                        action_steer = 2

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False
            self.avoidance_quadrant = 0
            self.avoidance_center = [0,0]
            self.init_pose = [state[0],state[1]]
            self.oriented = False

            # print(state[0])
            for i in range(1,5):
                self.centers[i-1][0] = simulator.param_dict['terrain_params'][i][0]
                self.centers[i-1][1] = simulator.param_dict['terrain_params'][i][1]
            
            # print(self.centers , self.init_pose)
            def check_quadrant(x1,y1):
                if(x1 == 0 or y1 == 0):
                    return 0
                if x1 > 0:
                    if y1 > 0:
                        return 1
                    else:
                        return 4
                elif x1 < 0:
                    if y1 > 0:
                        return 2
                    else:
                        return 3

            for i in range(4):
                q1 = check_quadrant(self.init_pose[0], self.init_pose[1])
                q2 = check_quadrant(self.centers[i][0],self.centers[i][1])
                # print(q1,q2)
                if(q1 == q2):
                    self.avoidance_center = self.centers[i]
                    self.avoidance_quadrant = check_quadrant(self.init_pose[0],self.init_pose[1])
                    break
            # print(self.init_pose, self.oriented, self.avoidance_quadrant, self.avoidance_center)
           
            for t in range(TIMESTEPS):
                if(np.abs(state[1]) < self.THRESHOLD_Y and np.abs(state[3]) < self.THRESHOLD_ANGLE):
                    self.oriented = True
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
