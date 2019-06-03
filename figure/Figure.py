import numpy as np
from skimage import draw

COLORS = {
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0)
    }

SHAPES = ["circle", "rectangle", "triangle"]

SIZES = ["small", "medium", "large"]

def drawcircle(figure, image):
    radius = (figure.pos[0][1] - figure.pos[0][0])/2
    centerrow = figure.pos[0][0] + radius
    centercol = figure.pos[1][0] + radius
    coords = draw.circle(centerrow, centercol, radius)
    draw.set_color(image, coords, figure.color[1])

def drawrectangle(figure, image):
    vertices_row = [figure.pos[0][0], figure.pos[0][1], figure.pos[0][1], figure.pos[0][0]]
    vertices_col = [figure.pos[1][0], figure.pos[1][0], figure.pos[1][1], figure.pos[1][1]]
    coords = draw.polygon(vertices_row, vertices_col, image.shape)
    draw.set_color(image, coords, figure.color[1])


def drawtriangle(figure, image):
    vertices_row = [figure.pos[0][1], figure.pos[0][0], figure.pos[0][1]]
    vertices_col = [figure.pos[1][0], figure.pos[1][0] + (figure.pos[1][1] - figure.pos[1][0])/2, figure.pos[1][1]]
    coords = draw.polygon(vertices_row, vertices_col, image.shape)
    draw.set_color(image, coords, figure.color[1])


class Figure(object):

    def __init__(self, shape, color, pos, size=None):
        self.shape = shape
        self.color = color  # (name, (r,g,b))
        self.pos = pos  # as simple bounding box in the form ((r0, r1), (c0, c1))
        self.size = size  # we only set the size from outside to generate the caption/description

    def draw(self, image):
        """
        Draw the figure on an image
        :param image: image array
        """
        if self.shape == "circle":
            drawcircle(self, image)
        elif self.shape == "rectangle":
            drawrectangle(self, image)
        elif self.shape == "triangle":
            drawtriangle(self, image)

    def position_label(self, imagesize):
        """
        Return the position label based on the coordinates of the bounding box of the shape. The image is devided
        into 4 areas: top left, top right, bottom left, bottom right
        :param imagesize: rows and cols of the image
        :return: a label for the position
        """
        # rows and cols of the image
        rows = imagesize[0]
        cols = imagesize[1]

        # determine middle row and col
        mid_row = int(np.floor(rows / 2))
        mid_col = int(np.floor(cols / 2))

        # Check which box the shape belongs to and assign a label
        horizontal_pos = ""
        vertical_pos = ""

        bounding_box = self.pos
        if bounding_box[0][0] <= mid_row and bounding_box[0][1] <= mid_row:
            vertical_pos = "top"
        elif bounding_box[0][0] > mid_row and bounding_box[0][1] > mid_row:
            vertical_pos = "bottom"

        if bounding_box[1][0] <= mid_col and bounding_box[1][1] <= mid_col:
            horizontal_pos = "left"
        elif bounding_box[1][0] > mid_col and bounding_box[1][1] > mid_col:
            horizontal_pos = "right"

        if horizontal_pos == "" and vertical_pos == "":
            return "center"

        return " ".join([vertical_pos, horizontal_pos]).strip()

    def generate_description(self, imagesize):
        size = self.size if self.size else ""
        shape_name = self.shape
        color_name = self.color[0]
        pos = self.position_label(imagesize)
        description = "A " + size + " " + color_name + " " + shape_name + " at the " + pos
        return description


    @classmethod
    def overlapping(cls, fig1, fig2):
        """
        Check if two figures overlap according to their bounding boxes (2D space)
        :param fig1: the first figure
        :param fig2: the second figure
        :return: True if the bounding boxes of the figures overlap, False if not
        """

        def overlapping1D(box1, box2):
            (min1, max1) = box1
            (min2, max2) = box2
            return max1 >= min2 and max2 >= min1

        if overlapping1D(fig1.pos[0], fig2.pos[0]) and overlapping1D(fig1.pos[1], fig2.pos[1]):
            return True
        else:
            return False

