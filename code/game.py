# -*- coding: utf-8 -*-
import pygame, sys
from level import Level
from settings import screen_width, screen_height
import numpy as np
import math
import pygame.surfarray as surfarray

class Game:
    def __init__(self,levelnumber=1):
        
        self.screen = pygame.display.set_mode((screen_width,screen_height))   
        self.time = 0
        # game attributes
        self.max_level = 1
        self.max_health = 1
        self.cur_health = 1
                
        self.levelnumber = levelnumber
        
        self.create_level()
        
    def create_level(self):
        self.level = Level(self.levelnumber,self.screen,self.change_health)
        
    def change_health(self,amount):
        self.cur_health += amount
        
    def check_game_over(self):
        if self.cur_health <= 0:
            self.level_bg_music.stop()
            self.level.gameover=True
                    
        
    def check_win(self):
        if self.level.win:
            self.level_bg_music.stop()
        
    def reset(self):
        self.level = Level(self.levelnumber,self.screen,self.change_health)
        self.cur_health = 1
        self.time=0
        
    def render(self):
        self.screen.fill('grey')
        self.level.render()
    
    def getObserv(self):
        return surfarray.array3d(self.screen)
    
    
    def run(self,useAgent,action):
        
        
        #left, right, jump, left+jump, right+jump
        
        actions = {pygame.K_RIGHT:False,pygame.K_LEFT:False,pygame.K_SPACE:False}
        if(action==0):
            actions[pygame.K_RIGHT]=True
        if(action==1):
            actions[pygame.K_SPACE]=True
            actions[pygame.K_RIGHT]=True
        
        """
        if(action==1 or action==3):
            actions[pygame.K_RIGHT]=True
        if(action==0 or action==4):
            actions[pygame.K_LEFT]=True
        if(action==2 or action==3 or action==4):
            actions[pygame.K_SPACE]=True
        """
        self.level.run(useAgent,actions)
        self.check_game_over()
        self.time+=1
        
        

#### AGENT UTILITIES

    def getReward(self):
        distanceReward = self.get_distance_to_end()
        return 5000-distanceReward-self.time*3 + (int(self.get_win())*5000) - (int(self.get_gameover())*5000)

    def get_distance_to_end(self):
        
        return self.rect_distance(self.level.player.sprite.rect,self.level.goal.sprite.rect)

    def rect_distance(self,rect1, rect2):
        x1, y1 = rect1.topleft
        x1b, y1b = rect1.bottomright
        x2, y2 = rect2.topleft
        x2b, y2b = rect2.bottomright
        left = x2b < x1
        right = x1b < x2
        top = y2b < y1
        bottom = y1b < y2
        if bottom and left:
            return math.hypot(x2b-x1, y2-y1b)
        elif left and top:
            return math.hypot(x2b-x1, y2b-y1)
        elif top and right:
            return math.hypot(x2-x1b, y2b-y1)
        elif right and bottom:
            return math.hypot(x2-x1b, y2-y1b)
        elif left:
            return x1 - x2b
        elif right:
            return x2 - x1b
        elif top:
            return y1 - y2b
        elif bottom:
            return y2 - y1b
        else:  # rectangles intersect
            return 0.00000001




    def get_done(self):
        #if game needs reset (win or gamover)
        return self.level.win or self.level.gameover or self.time>1000
    
    def get_win(self): return self.level.win
    
    def get_gameover(self): return self.level.gameover or self.time>1000

