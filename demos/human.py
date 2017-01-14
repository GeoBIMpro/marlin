"""
This allows a human to control the driver from stdin.
"""
import sys
from os import path
from random import choice

MY_DIR = path.dirname(path.abspath(__file__))
sys.path.insert(0, path.abspath(MY_DIR + '/..'))
from marlin import Game

game = Game(lidar_mode=False)
while not game.is_over():
    print("""
Enter 0 to change nothing, 1 to adjust the steering wheel to the right, 2 to 
move the steering wheel left, 3 to accelerate, 4 to brake.""")
    image, velocity, steering = game.get_state()
    print("current velocity", velocity, "|", "steering angle", steering)
    game.do_action(int(input()))
