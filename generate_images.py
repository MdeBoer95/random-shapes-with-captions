import matplotlib.image as mpimg
import numpy as np
import figures_random
import argparse
import csv
import os
from Figure import Figure
from config import SCConfig

BACKGROUND_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}

IMG_FORMAT = ".png"

CSVHEADER = ["file_name", "caption"]

def generate_image_with_caption(imageshape, maxshapes, allowoverlap=False, allowclipping=False,
                                backgroundcolor=BACKGROUND_COLORS["white"], exclude_stmts=[]):

    img = np.zeros(imageshape, dtype=np.double)
    imgsize = (img.shape[0], img.shape[1])

    # set the background color for all pixels
    for x in range(0, imgsize[0]):
        for y in range(0, imgsize[1]):
            img[x, y, :] = backgroundcolor

    descriptions = []
    figures = []

    # generate random figures until we have 'maxshapes' figures. Note that this approach can lead to a long runtime
    # if the probability of overlap is high since we resample every time the shape/figure doesn't fit
    drawn_shapes = 0
    while drawn_shapes < maxshapes:
        figure = figures_random.randomfigure(imgsize, exclude_stmts)
        if (allowoverlap or not isoverlapping(figure, figures)) and (allowclipping or not exceedesimagebounds(figure,
                                                                                                           imgsize)):
            figures.append(figure)
            figure.draw(img)
            descriptions.append(figure.generate_description(imgsize))
            drawn_shapes += 1

    caption = generate_caption(descriptions)
    return img, caption


def generate_caption(listofdescriptions):
    return '\n'.join(listofdescriptions)


def isoverlapping(figure, figures):
    for ifig in figures:
        if Figure.overlapping(figure, ifig):
            return True
    return False


def exceedesimagebounds(figure, imagesize):
    boundingbox = figure.pos
    return boundingbox[0][1] > imagesize[0] or boundingbox[1][1] > imagesize[1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_file",
                        default="config/default_config.json",
                        type=str,
                        required=False,
                        help="The config file that defines the parameters")
    parser.add_argument("--output_dir",
                        default="output",
                        type=str,
                        required=False,
                        help="The output directory where the dataset will we written")

    args = parser.parse_args()
    config = SCConfig.from_json(args.config_file)

    np.random.seed(config.random_seed)

    if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
        raise ValueError("Output directory ({}) already exists and is not empty.".format(args.output_dir))
    os.makedirs(args.output_dir)

    imagedir = os.path.join(args.output_dir,"images")
    os.makedirs(imagedir)

    with open(os.path.join(args.output_dir, "image_captions.csv"), "w") as csvf:
        csvwriter = csv.writer(csvf)
        csvwriter.writerow(CSVHEADER)

        imgsize = config.image_size
        imgshape = (imgsize[0], imgsize[1], 3)

        for i in range(config.num_images):
            # generate image and caption
            img, caption = generate_image_with_caption(imgshape, config.shapes_per_image, allowoverlap=config.allow_overlap,
                                                       allowclipping=config.allow_clipping,
                                                       backgroundcolor=config.background_color,
                                                       exclude_stmts=config.exclude_stmts)
            # store image
            imgfilename = os.path.join(imagedir, "img" + str(i) + IMG_FORMAT)
            mpimg.imsave(imgfilename, img)
            # store file name and caption in csv file
            csvwriter.writerow([imgfilename, caption])
