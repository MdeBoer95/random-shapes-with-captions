class DatasetStatistics(object):

    def __init__(self):
        self.num_shapes = {
            "rectangle": 0,
            "circle": 0,
            "triangle": 0
        }
        self.num_colors = {
            "red": 0,
            "blue": 0,
            "green": 0,
            "yellow": 0
        }
        self.num_sizes = {
            "small": 0,
            "medium": 0,
            "large": 0
        }
        self.num_positions = {
            "top right": 0,
            "top left": 0,
            "bottom right": 0,
            "bottom left": 0,
            "top": 0,
            "bottom": 0,
            "left": 0,
            "right": 0,
            "center": 0
        }

    def update(self, figures, imagesize=[256, 256]):
        for figure in figures:
            self.num_shapes[figure.shape] += 1
            self.num_colors[figure.color[0]] += 1
            self.num_sizes[figure.size] += 1
            self.num_positions[figure.position_label(imagesize)] += 1



    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        l = [
            self.num_shapes.__repr__(),
            self.num_colors.__repr__(),
            self.num_sizes.__repr__(),
            self.num_positions.__repr__()
        ]
        return ", ".join(l)


