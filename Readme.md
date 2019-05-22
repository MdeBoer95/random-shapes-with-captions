# Random Shapes-Caption Datasets

This repository contains an implementation for generating simple, artificial image-caption datasets. 

The generated images contain figures which can have three types of different shapes (*rectangle*, *triangle*, *circle*), one of four different colors (*blue*,*red*,*green*,*yellow*) and one of the sizes (*small*,*medium*,*large*). The positions of the shapes in an image are randomly sampled. The captions for the images always follow the same pattern. Each row(sentence) of the a caption describes one of the figures in the images in terms of its shapename, color, size and position. The position can be one of the following (top left, top right, bottom left, bottom right, left, right, top, bottom, center). The image is divided into approximately four quadrants and position labels are assigned accordingly.

The purpose of the datasets is to use them for debugging sophisticated models. Since the generated datasets are very simple, any properly working model should be able to solve the them.

## Requirements
The script requires the following packages:
- matplotlip (3.0.3)
- numpy (1.16.3)
- scikit-image (0.15.0)

It will probably also work with older versions but has not been tested.

## Generating Datasets
A dataset can be generated via
```
python generate_images.py [--parameter1 val1][--parameter2 val2] ... (see table below)
```
This will create a folder ```images``` that contains the generated images and a csv-file ```image_captions.csv``` that contains the captions for the images in the folder specified by ```--output```.
The ```image_captions.csv``` file has one row for the relative path to an image and one row for the corresponding caption.
The following table lists the parameters that can be used with the generate_images.py command

**Parameters:**

| Name | Description | Default value |
| --- | --- | --- |
| --num\_images | Number of generated images.  | 50 |
| --image\_size | Size of the images | 256 256 | 
| --output\_dir | The output directory where the dataset will we written | output | 
| --shapes\_per\_image | Number of shapes per generated image| 3 | 
| --background\_color | Background color of the generated images | 255 255 255|
| --allow\_overlap | Whether the figures can overlap | False | 
| --allow\_clipping| Whether the figures can exceed the image borders | False | 
| --random\_seed | A random seed for the image generation| None | 



