import numpy as np
from .. import maps
from ..core import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def make_wt(map_id):
    item = getattr(maps, map_id)
    world = World()
    track = Track(item.x_t, item.y_t, item.e_t)
    track.add_to(world)
    return world, track

def make_preview(track, world=None, title=None):
    fig = Figure(figsize=(10, 10))
    if title: fig.suptitle(title)

    canvas = FigureCanvas(fig)
    ax = fig.gca()

    ts = np.linspace(0.0, track.e_t, num=10000)
    x = [track.x_t(t) for t in ts]
    y = [track.y_t(t) for t in ts]
    ax.plot(x, y)

    if not world: world = World()
    track.add_to(world)
    x = [cone['x'] for cone in world.cones]
    y = [cone['y'] for cone in world.cones]
    ax.scatter(x, y)

    top, bottom = min(y), max(y)
    left, right = min(x), max(x)
    size = max(bottom - top + 10, right - left + 10) / 2.0

    center_y = (bottom + top) / 2.0
    center_x = (right + left) / 2.0
    ax.set_xlim([center_x-size, center_x+size])
    ax.set_ylim([center_y-size, center_y+size])

    canvas.draw()
    image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(canvas.get_width_height()[::-1] + (3,))
    return image
