"""
This is a dueling DQN controller which takes the image part of the state (for simplicity, it 
ignores the velocity and steering angle).
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
        self.game = Game(lidar_mode=False)
        self.total_reward = False
        self.game.reset()

    @property
    def name(self): return "QL4KGame"
    
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

# Dueling DQN architecture (see https://arxiv.org/pdf/1511.06581v3.pdf)
from keras.layers import *
from keras.models import *
from keras import backend as K
from qlearning4k import Agent

ql4kgame = QL4KGame()
nb_frames = 2
nb_actions = ql4kgame.nb_actions

x_in = Input(shape=(nb_frames, 240, 360))

adv = Convolution2D(8, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(x_in)
adv = Convolution2D(16, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(adv)
adv = Convolution2D(32, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(adv)
adv = Convolution2D(64, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(adv)
adv = Convolution2D(128, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(adv)
adv = Convolution2D(256, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(adv)
adv = Flatten()(adv)
adv = Dense(nb_actions)(adv)
adv = Lambda(lambda x: x - K.mean(x, axis=1, keepdims=True))(adv)

val = Convolution2D(8, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(x_in)
val = Convolution2D(16, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(val)
val = Convolution2D(32, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(val)
val = Convolution2D(64, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(val)
val = Convolution2D(128, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(val)
val = Convolution2D(256, 3, 3, subsample=(2,2), activation='relu', dim_ordering='th')(val)
val = Flatten()(val)
val = Dense(1)(val)
val = RepeatVector(nb_actions)(val)
val = Flatten()(val)

y_out = merge([adv, val], mode='sum')

model = Model(input=x_in, output=y_out)
model.compile(optimizer='rmsprop', loss='mse')

agent = Agent(model=model, memory_size=-1, nb_frames=nb_frames)
agent.train(ql4kgame, batch_size=64, nb_epoch=300, gamma=0.7)
model.save("dqn_model.h5")
agent.play(ql4kgame)
