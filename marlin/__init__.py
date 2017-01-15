from . import core
from . import maps
from . import utils
from random import choice

class Game:

    def __init__(self, lidar_mode=True):
        self.num_actions = 5
        self.on_track = True
        self.right_dir = True
        self.lidar_mode = lidar_mode
        self.reset()

    def reset(self):
        drive = core.Drive()
        world, track = utils.make_wt(choice(maps.MAP_IDS))
        world.set_lidar(self.lidar_mode)
        drive.x, drive.y, drive.a = track.get_pose(0.0)
        self.drive, self.world, self.track = drive, world, track

    def is_won(self):
        drive, world, track = self.drive, self.world, self.track
        end_x, end_y, _ = track.get_pose(track.e_t)
        if abs(end_x - drive.x) + abs(end_y - drive.y) < 5.0:
            return True
        return False

    def is_over(self):
        if self.is_won(): return True
        if self.on_track and self.right_dir:
            return False
        return True

    def get_state(self):
        drive, world, track = self.drive, self.world, self.track
        return world.render((drive.x, drive.y, drive.a)), drive.v, drive.s

    def get_score(self):
        if self.is_won(): return 100.0
        if self.on_track and self.right_dir:
            return self.drive.v + 1.0 / (1.0 + self.d)
        return 0.0

    def do_action(self, action):
        drive, world, track = self.drive, self.world, self.track

        if action == 0:
            drive.set_steering(0.1)
        elif action == 1:
            drive.set_steering(0.0)
        elif action == 2:
            drive.set_steering(-0.1)
        elif action == 3:
            drive.set_velocity(5.0)
        elif action == 4:
            drive.set_velocity(2.5)
        else: raise "Unsupported action."
        drive.step()

        pose = [drive.x, drive.y, drive.a]
        self.on_track, self.right_dir, self.d, self.da = track.evaluate(pose)
        world.set_message({
            "x": round(drive.x, 2),
            "y": round(drive.y, 2),
            "a": round(drive.a, 2),
            "v": round(drive.v, 2),
            "s": round(drive.s, 2)
        })
