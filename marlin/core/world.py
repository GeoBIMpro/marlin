from time import sleep
from io import BytesIO
from requests import post
from scipy.misc import imread, imsave

class World:
    
    def __init__(self):
        self.cones = []

    def add_cone(self, x, y):
        self.cones.append({"x":x,"y":y})

    def render(self, pose):
        while True:
            try:
                url = "http://localhost:3000/"
                pose = (pose[0], pose[1], pose[2])
                payload = {"cones": self.cones, "pose": pose}
                response = post(url, json=payload)
                return imread(BytesIO(response.content))
            except:
                print("Connection lost. Retrying in 3 seconds...")
                sleep(3)
