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


class Videos2Frames(OSUtils):

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

    def convert_videos_to_frames(
        self,
        rotation: int = 270,
        crop: dict = dict(left=420, right=420, top=0, bottom=0),
        resize: tuple = (600, 600),
        test_size=0.25
    ) -> None:
        """ Convert videos to frames (with train and test set split). """
        self._make_dirs()
        for video, person in zip(self.videos, self.people):
            video = cv2.VideoCapture(video)
            success, image = video.read()
            count = 0
            while success:
                image = self._preprocess_frame(image, rotation=rotation, resize=resize)
                if self._choose_dataset(test_size=test_size):
                    cv2.imwrite(os.path.join(self.datasets[0], person, '%d.jpg' % count), image)
                else:
                    cv2.imwrite(os.path.join(self.datasets[1], person, '%d.jpg' % count), image)
                success, image = video.read()
                count += 1

    @staticmethod
    def _preprocess_frame(
        frame: np.ndarray,
        rotation: int = 270,
        crop: dict = dict(left = 420, right=420, top=0, bottom=0),
        resize: tuple = (600, 600)        
    ):
        """ Preprocess frame captured from video. """
        if rotation:
            frame = imutils.rotate(frame, rotation)
        if crop:
            frame = frame[
                crop['bottom']:frame.shape[0]-crop['top'],
                crop['left']:frame.shape[1]-crop['right'],
                :]
        if resize:
            frame = cv2.resize(frame, resize)
        return frame

    @staticmethod
    def _choose_dataset(test_size=0.25) -> bool:
        """ """
        return np.random.choice([True, False], size=1, p=[1 - test_size, test_size])

    def _make_dirs(self) -> None:
        """ Create directories dedicated to specific face recognition system. """
        for dataset in self.datasets:
            for person in self.people:
                self.make_dirs(os.path.join(dataset, person))
