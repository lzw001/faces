import os
import warnings
import numpy as np
import cv2
import imutils

from .utils import OSUtils, ImageUtils


class Videos2Datasets(OSUtils, ImageUtils):

    def __init__(
        self,
        videos: list,
        people: list,
        train_dir: str = 'data/train',
        test_dir: str = 'data/test'
    ) -> None:

        self.videos = videos
        self.people = people
        self.datasets = [train_dir, test_dir]

    def train_test_split(self, test_size=0.25, *args, **kwargs) -> None:
        """ Prepare train and test sets which will be used in
        training procedure.

        :param test_size:
        :param *args, **kwargs:

        :return: None
        """
        self._make_dirs()
        for video, person in zip(self.videos, self.people):
            # capture image
            video = cv2.VideoCapture(video)
            success, image = video.read()
            count = 0
            while success:
                image = self.preprocess_image(image, *args, **kwargs)
                dataset = self._choose_dataset(test_size=test_size)
                cv2.imwrite(
                	os.path.join(self.datasets[dataset], person, '%d.jpg' % count),
                	image
                )
                success, image = video.read()
                count += 1

    def _make_dirs(self) -> None:
        """ Create directories dedicated to specific datasets. """
        for dataset in self.datasets:
            for person in self.people:
                self.make_dirs(os.path.join(dataset, person))

    @staticmethod
    def _choose_dataset(test_size=0.25) -> bool:
        """ Choose dataset for specific frame. """
        return np.random.choice([0, 1], size=1, p=[1-test_size, test_size])
