"""
This is a random controller which chooses the 5 actions uniformly.
"""
import sys
from os import path
from random import choice

MY_DIR = path.dirname(path.abspath(__file__))
sys.path.insert(0, path.abspath(MY_DIR + '/..'))
from marlin import Game

game = Game()
while not game.is_over():
    image, velocity, steering = game.get_state()
    game.do_action(choice(range(game.num_actions)))
