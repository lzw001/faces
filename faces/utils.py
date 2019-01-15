import os
import glob
import warnings
import numpy as np
import cv2
import imutils

from typing import Union

class OSUtils(object):

    def make_dirs(self, directory: str) -> None:
        """ Check whether directory exists. If not,
        then create the directory with os.makedirs()

        :param directory:
        :type directory: str

        :return: None
        """
        if not os.path.isdir(directory):
            os.makedirs(directory)


class ImageUtils(object):

    def preprocess_image(
        self,
        image: np.ndarray,
        rotation: int = 270,
        crop: dict = dict(left=420, right=420, top=0, bottom=0),
        resize: tuple = (600, 600)
    ):
        """ Process image which was represent as np.ndarray. Possible
        operations are: rotation, crop and resize.

        :param image:
        :param rotation:
        :param crop:
        :param resize:

        :return: image
        """
        if rotation:
            image = imutils.rotate(image, rotation)
        if crop:
            image = image[
                crop['bottom']:image.shape[0]-crop['top'],
                crop['left']:image.shape[1]-crop['right'],
                :]
        if resize:
            image = cv2.resize(image, resize)
        return image

    def get_paths_and_classes(
        self,
        path_to_images: str,
        path_to_classes: list = ['anna', 'lukasz'],
        images_extension: str = '*.jpg'
    ) -> Union[list, list]:
        """ Get paths to images and corresponding classes. This method
        will be used in preparation of datasets and/or transform images
        from specific directories.

        :param path_to_images:
        :param path_to_classes:
        :param images_extension:

        :return: images, classes
        """
        images, classes = [], []
        for path_to_class in path_to_classes:
            images_in_dir = glob.glob(
                os.path.join(path_to_images, path_to_class, images_extension)
            )
            images.extend(images_in_dir)
            classes.extend([path_to_class for _ in range(len(images_in_dir))])
        return images, classes
