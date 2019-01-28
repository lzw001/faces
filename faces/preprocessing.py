import os
import glob
import warnings
import numpy as np
import cv2
import imutils

from skimage import io, transform
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
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
    def _choose_dataset(test_size: float = 0.25) -> int:
        """ Choose dataset for specific frame. """
        return int(np.random.choice([0, 1], size=1, p=[1-test_size, test_size]))


class FacesDataset(Dataset):
    """FacesDataset will be used by models developed in PyTorch"""
    def __init__(self, path_to_images: str, transform=None):
        
        self.images = glob.glob(pathname=path_to_images)
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        """ """
        image_path = self.images[idx]
        image = io.imread(fname=image_path)
        if self.transform:
            image = self.transform(image)
        person = image_path.split('/')[-2]
        return image, person
