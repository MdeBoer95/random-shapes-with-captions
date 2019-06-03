import csv

STATS_CSVHEADER = ["color", "size", "shape", "position"]


class DatasetStatistics(object):

    def __init__(self):
        self.figures = []

    def update(self, figures):
        self.figures.extend(figures)

    def write_to_file(self, filepath, image_size=[256, 256]):
        with open(filepath, "w") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(STATS_CSVHEADER)

            for figure in self.figures:
                csvline = [figure.color[0], figure.size, figure.shape, figure.position_label(image_size)]
                csvwriter.writerow(csvline)




