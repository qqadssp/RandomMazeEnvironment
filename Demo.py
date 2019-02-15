import numpy as np
import matplotlib.pyplot as plt
from RandomMazeEnv import RandomMazeEnv
from ActionList import creat_action_list

env = RandomMazeEnv('./RandomMaze/Maze.x86_64')
env.seed(0)
ob, _, _, _ = env.reset()

action_list = creat_action_list()

for kv in action_list:
    step = kv[0]
    action = kv[1]
    for i in range(step):
        ob, reward, done, _ = env.step(action)
        print(action, reward, done)
#        if i > 0 and i % 40 == 0:
#            plt.imshow(ob)
#            plt.show()

env.close()

