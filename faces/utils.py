import os
import warnings
import numpy as np
import cv2
import imutils


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
