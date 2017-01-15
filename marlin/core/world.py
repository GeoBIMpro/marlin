from time import sleep
from io import BytesIO
from requests import post
from scipy.misc import imread, imsave

class World:
    
    def __init__(self):
        self.cones = []
        self.message = False
        self.lidar_mode = False

    def add_cone(self, x, y):
        self.cones.append({"x":x,"y":y})

    def set_lidar(self, lidar_mode):
        self.lidar_mode = lidar_mode

    def set_message(self, message):
        self.message = message

    def render(self, pose):
        while True:
            try:
                url = "http://localhost:3000/"
                pose = (pose[0], pose[1], pose[2])
                payload = {
                    "cones": self.cones, 
                    "pose": pose, 
                    "message": self.message,
                    "LIDAR_MODE": self.lidar_mode
                }
                response = post(url, json=payload)
                return imread(BytesIO(response.content))
            except:
                print("Connection lost. Retrying in 3 seconds...")
                sleep(3)
