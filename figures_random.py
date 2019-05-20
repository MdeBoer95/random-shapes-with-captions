import matplotlib.pyplot as plt
import numpy as np
import random
from Figure import Figure

COLORS = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0)
    }

SHAPES = ["circle", "rectangle", "triangle"]

SIZES = ["small", "middle", "large"]


def randomcolor():
    key = random.choice(list(COLORS.keys()))
    return key, COLORS[key]


def randomshape():
    return random.choice(SHAPES)


def randomsize():
    return random.choice(SIZES)


def randombox(imagesize, minrow=0, mincol=0, boxsize="middle"):
    """
    Get a random postion for a bounding box
    :return: coords of the bounding box in the form ((r0, r1), (c0, c1))
    """
    maxrow = imagesize[0]
    maxcol = imagesize[1]
    size_bounds = getsizebounds(imagesize)[boxsize]
    width = np.random.randint(size_bounds[0], size_bounds[1])

    r0 = np.random.randint(minrow, maxrow)
    r1 = r0 + width

    c0 = np.random.randint(mincol, maxcol)
    c1 = c0 + width

    return (r0, r1),(c0, c1)


def getsizebounds(imagesize):
    imgwidth = imagesize[0]

    size_bounds = {
        "small": (int(np.floor(imgwidth*0.05)), int(np.floor(imgwidth*0.12))),
        "middle": (int(np.floor(imgwidth*0.13)), int(np.floor(imgwidth*0.18))),
        "large": (int(np.floor(imgwidth*0.19)), int(np.floor(imgwidth*0.25)))
    }

    return size_bounds


def randomfigure(imagesize):
    shape = randomshape()
    size = randomsize()
    pos = randombox(imagesize, boxsize=size)
    color = randomcolor()
    return Figure(shape=shape, pos=pos, color=color, size=size)
