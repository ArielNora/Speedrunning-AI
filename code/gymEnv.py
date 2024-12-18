# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 12:47:00 2022

@author: Ariel Nora
"""

import gym
from gym import spaces
from game import Game
import numpy as np
import cv2

class MarioEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self,useAgent,nb_actions,levelnumber=1):
        super(MarioEnv, self).__init__()    # Define action and observation space
        
        #all possible actions
        self.action_space = spaces.Discrete(nb_actions)   
        
        #what is observed : position of player character
        #the position will be current/maximum to get a number between 0 and 1
        self.observation_space = spaces.Box(low=0,high=1,shape=(84,84), dtype=int)
        self.game = Game(levelnumber=levelnumber)
        self.useAgent = useAgent
        
    def preprocess(self,rgb):
        gray = np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
        gray /= 255
        res = cv2.resize(gray, dsize=(84, 84), interpolation=cv2.INTER_CUBIC)
        return np.array([np.float32(res)])
    
    def step(self, action):
        # Execute one time step within the environment
        
        if(self.useAgent):skip=4
        else:skip=1
        
        total_reward = 0.0
        done = False
        for i in range(skip):
            
            self.game.run(self.useAgent,action)
            
            obs = self.game.getObserv()
            obs = self.preprocess(obs)
            done = self.game.get_done()
            reward = self.game.getReward()
            total_reward += reward
        
            if done:
                break
            
        return obs, total_reward, done, {}
        
    def reset(self):
        # Reset the state of the environment to an initial state
        self.game.reset()
        self.render()
        return self.preprocess(self.game.getObserv())
        
        
    def render(self):
        # Render the environment to the screen
        self.game.render()











