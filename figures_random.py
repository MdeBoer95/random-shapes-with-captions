import numpy as np
import random
import itertools
from Figure import Figure

COLORS = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0)
    }

SHAPES = ["circle", "rectangle", "triangle"]

SIZES = ["small", "medium", "large"]


def randombox(imagesize, minrow=0, mincol=0, boxsize="medium"):
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
        "medium": (int(np.floor(imgwidth*0.13)), int(np.floor(imgwidth*0.18))),
        "large": (int(np.floor(imgwidth*0.19)), int(np.floor(imgwidth*0.25)))
    }

    return size_bounds


def attribute_combinations(exclude_statements=[]):
    """
    Get all allowed attribute combinations for the figures. The allowed combinations can be restricted by the
    exclude_statements property in the configs file.
    :param exclude_statements:
    :return:
    """
    excluded_combs = []
    for exclude_group in exclude_statements:
        # excluded tuples according to the given exclude-statement (COLOR, SIZE, SHAPE)
        # if no valid value is specified for an attribute we count it as wildcard (i.e. add all elements for that attr.)
        excluded_attr = [[exclude_group[0]] if exclude_group[0] in COLORS.keys() else list(COLORS.keys()),
                         [exclude_group[1]] if exclude_group[1] in SIZES else SIZES,
                         [exclude_group[2]] if exclude_group[2] in SHAPES else SHAPES]
        # all excluded combinations
        excluded_combs.extend(list(itertools.product(*excluded_attr)))

    attrs = [list(COLORS.keys()), SIZES, SHAPES]
    included_combs = set(itertools.product(*attrs)) - set(excluded_combs)
    return list(included_combs)


def randomfigure(imagesize, exclude_statements=[]):
    attrs = random.choice(attribute_combinations(exclude_statements))
    shape = attrs[2]
    size = attrs[1]
    pos = randombox(imagesize, boxsize=size)
    color = (attrs[0], COLORS[attrs[0]])
    return Figure(shape=shape, pos=pos, color=color, size=size)
