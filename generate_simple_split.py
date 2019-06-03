import matplotlib.image as mpimg
import numpy as np
import argparse
import csv
import os
import figure.figures_random as figures_random
from stats.stats import DatasetStatistics
from figure.Figure import Figure, COLORS
from config import SCConfig
from dataset_constants import BACKGROUND_COLORS, IMG_FORMAT, CAPTION_CSVHEADER


def generate_image_with_caption(imageshape, figure, allowclipping=False,
                                backgroundcolor=BACKGROUND_COLORS["white"]):

    img = np.zeros(imageshape, dtype=np.double)
    imgsize = (img.shape[0], img.shape[1])

    # set the background color for all pixels
    for x in range(0, imgsize[0]):
        for y in range(0, imgsize[1]):
            img[x, y, :] = backgroundcolor

    if allowclipping or not exceedesimagebounds(figure, imgsize):
        figure.draw(img)
        figure.generate_description(imgsize)

    caption = generate_caption(figure.generate_description(imgsize))
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


def generate_set(setname, combs, imgsize, allow_clipping, background_color, output_dir):
    setdir = os.path.join(output_dir, setname)
    os.makedirs(setdir)

    imagedir = os.path.join(setdir, "images")
    os.makedirs(imagedir)

    stats = DatasetStatistics()

    with open(os.path.join(setdir, "image_captions.csv"), "w") as setcsv:
        csvwriter = csv.writer(setcsv)
        csvwriter.writerow(CAPTION_CSVHEADER)

        imgshape = (imgsize[0], imgsize[1], 3)

        for i, comb in enumerate(combs):
            # generate image and caption
            pos = figures_random.randombox(imgsize, boxsize=comb[1])
            figure = Figure(color=(comb[0], COLORS[comb[0]]), size=comb[1], pos=pos, shape=comb[2])

            # sample random position for the figure until it fits
            while exceedesimagebounds(figure, imgsize) and not allow_clipping:
                pos = figures_random.randombox(imgsize, boxsize=comb[1])
                figure.pos = pos

            img, caption = generate_image_with_caption(imgshape, figure,
                                                       backgroundcolor=background_color)
            stats.update([figure])

            imgfilename = os.path.join(imagedir, "img" + str(i) + IMG_FORMAT)
            mpimg.imsave(imgfilename, img)
            # store file name and caption in csv file
            csvwriter.writerow([imgfilename, caption])

    stats.write_to_file(os.path.join(setdir, "dataset_statistics.csv"), imgsize)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_file",
                        type=str,
                        required=True,
                        help="The configs file that defines the parameters")
    parser.add_argument("--output_dir",
                        default="output",
                        type=str,
                        required=False,
                        help="The output directory where the dataset will we written")
    parser.add_argument("--split",
                        default=[80, 10, 10],
                        type=int,
                        nargs=3,
                        required=False,
                        help="Percentage of train, val, test split")

    args = parser.parse_args()
    config = SCConfig.from_json(args.config_file)

    np.random.seed(config.random_seed)

    if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
        raise ValueError("Output directory ({}) already exists and is not empty.".format(args.output_dir))
    os.makedirs(args.output_dir)

    combs = figures_random.attribute_combinations(exclude_statements=config.exclude_stmts)
    num_combs = len(combs)

    num_train_examples = int(np.floor((args.split[0]/100.0) * num_combs))
    num_val_examples = int(np.floor(args.split[1]/100.0 * num_combs))
    num_test_examples = int(np.floor(args.split[2]/100.0 * num_combs))

    num_examples = num_train_examples + num_val_examples + num_test_examples
    # adjust if the split doesn't cover all combinations by adding the remaining one to the training set
    if num_examples != num_combs:
        num_train_examples += num_combs - num_examples

    # randomly shuffle the list of combinations
    np.random.shuffle(combs)

    generate_set("train", combs[0: num_train_examples], config.image_size, config.allow_clipping,
                 config.background_color, args.output_dir)

    generate_set("val", combs[num_train_examples: num_train_examples + num_val_examples], config.image_size,
                 config.allow_clipping,
                 config.background_color, args.output_dir)

    generate_set("test", combs[num_train_examples + num_val_examples:], config.image_size, config.allow_clipping,
                 config.background_color, args.output_dir)
