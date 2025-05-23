import pygame
import numpy as np
from gymEnv import MarioEnv
import matplotlib.pyplot as plt
import torch
from agent import Mario
from logger import MetricLogger
import sys



def main(level=1):
    
    pygame.init()
    useAgent = True
    nbActions=3
    pygame.init()

    levelnumber = level



    env = MarioEnv(useAgent,nbActions,levelnumber)

    use_cuda = torch.cuda.is_available()
    print(f"Using CUDA: {use_cuda}")
    print()

    mario = Mario(state_dim=(1, 84, 84), action_dim=env.action_space.n)

    logger = MetricLogger()    
            
    episodes = 400
    for e in range(episodes):

        state = env.reset()
        test = state.shape
        #print()
        # Play the game!
        while True:
            
            #print(state.shape,end="    ")
            # Run agent on the state
            action = mario.act(state)
            # Agent performs action
            next_state, reward, done, info = env.step(action)
            # Remember
            mario.cache(state, next_state, action, reward, done)

            # Learn
            q, loss = mario.learn()
            print("curr_step: ",mario.curr_step,"q,loss: ",q,loss)

            # Logging
            logger.log_step(reward, loss, q)

            # Update state
            state = next_state
            env.render()
            pygame.display.update()
            # Check if end of game
            if done:
                break

        logger.log_episode()
        if e % 10 == 0:
            logger.record(episode=e, epsilon=mario.exploration_rate, step=mario.curr_step)
        
    pygame.quit()


if __name__ == "__main__":

    args = sys.argv[1:]
    print(args)

    main(int(args[0]))