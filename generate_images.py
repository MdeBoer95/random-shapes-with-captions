import matplotlib.image as mpimg
import numpy as np
import figures_random
import argparse
import csv
import os
from Figure import Figure

BACKGROUND_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}

IMG_FORMAT = ".png"

CSVHEADER = ["file_name", "caption"]

def generate_image_with_caption(imageshape, maxshapes, allowoverlap=False, allowclipping=False,
                                backgroundcolor=BACKGROUND_COLORS["white"]):

    img = np.zeros(imageshape, dtype=np.double)
    imgsize = (img.shape[0], img.shape[1])

    # set all pixel to the background color
    for x in range(0, imgsize[0]):
        for y in range(0, imgsize[1]):
            img[x, y, :] = backgroundcolor

    descriptions = []
    figures = []

    # generate random figures until we have 'maxshapes' figures. Note that this approach can lead to a long runtime
    # if the probability of overlap is high
    drawn_shapes = 0
    while drawn_shapes < maxshapes:
        figure = figures_random.randomfigure(imgsize)
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

    ## Required parameters
    parser.add_argument("--num_images",
                        default=50,
                        type=int,
                        required=False,
                        help="Number of generated images")
    parser.add_argument("--image_size",
                        default=(255, 255),
                        type=tuple,
                        required=False,
                        help="Size of the image")
    parser.add_argument("--output_dir",
                        default="output",
                        type=str,
                        required=False,
                        help="The output directory where the dataset will we written.")
    parser.add_argument("--shapes_per_image",
                        default=3,
                        type=int,
                        required=False,
                        help="Number of shapes per generates image.")
    parser.add_argument("--background_color",
                        default=BACKGROUND_COLORS["white"],
                        type=tuple,
                        required=False,
                        help="Backgroundcolor of the generated images")
    parser.add_argument("--allow_overlap",
                        default=False,
                        type=bool,
                        required=False,
                        help="Whether the figure can overlap")
    parser.add_argument("--random_seed",
                        default=None,
                        type=int,
                        required=False,
                        help="A random seed for the image generation")

    args = parser.parse_args()
    np.random.seed(args.random_seed)

    if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
        raise ValueError("Output directory ({}) already exists and is not empty.".format(args.output_dir))
    os.makedirs(args.output_dir, exist_ok=True)

    imagedir = os.path.join(args.output_dir,"images")
    os.makedirs(imagedir)

    with open(os.path.join(args.output_dir, "image_captions.csv"), "w") as csvf:
        csvwriter = csv.writer(csvf)
        csvwriter.writerow(CSVHEADER)

        imgsize = args.image_size
        imgshape = (imgsize[0], imgsize[1], 3)

        for i in range(args.num_images):
            # generate image and caption
            img, caption = generate_image_with_caption(imgshape, args.shapes_per_image, allowoverlap=args.allow_overlap,
                                                       backgroundcolor=args.background_color)
            # store image
            imgfilename = os.path.join(imagedir, "img" + str(i) + IMG_FORMAT)
            mpimg.imsave(imgfilename, img)
            # store file name and caption in csv file
            csvwriter.writerow([imgfilename, caption])