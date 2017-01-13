"""
This is a simple DQN controller which takes the image part of the state (for simplicity, it ignores
the velocity and steering angle).
"""

# First let's wrap the internal game interface with a qlearning4k compatible interface
import sys
from os import path
MY_DIR = path.dirname(path.abspath(__file__))
sys.path.insert(0, path.abspath(MY_DIR + '/..'))
from marlin import Game

reward_log = open("dqn_rewards.txt", "wt")
class QL4KGame(object):
    
    def __init__(self):
        self.game = Game()
        self.total_reward = False
        self.game.reset()

    @property
    def name(self): return "kGame"
    
    @property
    def nb_actions(self): return self.game.num_actions
    
    def reset(self):
        if self.total_reward:
            reward_log.write(str(self.total_reward) + "\n")
            reward_log.flush()
        self.total_reward = 0.0
        self.game.reset()

    def play(self, action):
        self.game.do_action(action)
        self.total_reward += self.get_score()

    def get_state(self): return self.game.get_state()[0][:,:,0] / 127.5 - 1.0
    def get_score(self): return self.game.get_score()
    def is_over(self): return self.game.is_over()
    def is_won(self): return self.game.is_won()
    def get_frame(self): return self.get_state()
    def draw(self): return self.get_state()
    def get_possible_actions(self): return range(self.nb_actions)

# Now let's hand over all the learning / replay stuff to ql4k and off we go!
from keras.models import Sequential, load_model
from keras.layers import *
from keras.optimizers import *
from qlearning4k import Agent

ql4kgame = QL4KGame()

nb_frames = 2
nb_actions = ql4kgame.nb_actions
model = Sequential()
model.add(Convolution2D(8, 3, 3, activation='relu', dim_ordering="th", input_shape=(nb_frames, 256, 256)))
model.add(Convolution2D(16, 3, 3, subsample=(2,2), activation='relu', dim_ordering="th"))
model.add(Convolution2D(16, 3, 3, subsample=(2,2), activation='relu', dim_ordering="th"))
model.add(Convolution2D(32, 3, 3, subsample=(2,2), activation='relu', dim_ordering="th"))
model.add(Convolution2D(32, 3, 3, subsample=(2,2), activation='relu', dim_ordering="th"))
model.add(Convolution2D(64, 3, 3, subsample=(2,2), activation='relu', dim_ordering="th"))
model.add(Convolution2D(64, 3, 3, subsample=(2,2), activation='relu', dim_ordering="th"))
model.add(Flatten())
model.add(Dense(nb_actions))
model.compile(RMSprop(), 'MSE')

agent = Agent(model=model, memory_size=10000, nb_frames=nb_frames)
agent.train(ql4kgame, batch_size=64, nb_epoch=200, gamma=0.7)
agent.play(ql4kgame)
