import json


class SCConfig(object):

    def __init__(self, num_images, image_size, shapes_per_image, background_color, allow_overlap, allow_clipping,
                 random_seed, exclude_stmts):
        self.num_images = num_images
        self.image_size = image_size
        self.shapes_per_image = shapes_per_image
        self.background_color = background_color
        self.allow_overlap = allow_overlap
        self.allow_clipping = allow_clipping
        self.random_seed = random_seed
        self.exclude_stmts = exclude_stmts

    @classmethod
    def from_json(cls, filepath):
        with open(filepath) as f:
            config_json = json.load(f)
            num_images = config_json["num_images"]
            image_size = config_json["image_size"]
            shapes_per_image = config_json["shapes_per_image"]
            background_color = config_json["background_color"]
            allow_overlap = config_json["allow_overlap"]
            allow_clipping = config_json["allow_clipping"]
            random_seed = config_json["random_seed"]
            exclude_stmts = config_json["exclude_statements"]
            return SCConfig(num_images, image_size, shapes_per_image, background_color, allow_overlap, allow_clipping,
                            random_seed, exclude_stmts)
