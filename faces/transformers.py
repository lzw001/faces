import numpy as np
import os
import glob
import cv2
import dlib

from typing import Union
from tqdm import tqdm
from sklearn.metrics import euclidean_distances
from .utils import ImageUtils


class FaceLandmarksTransformer(ImageUtils):

    def __init__(self, face_landmarks_predictor: str) -> None:

        self.face_landmarks_predictor = dlib.shape_predictor(
            face_landmarks_predictor)
        self.face_detector = dlib.get_frontal_face_detector()

    def transform_from_directory(
        self,
        path_to_images: str,
        path_to_classes: list = ['anna', 'lukasz'],
        images_extension: str = '*.jpg',
        landmarks_flatten_dimension: int = int(1/2 * (68 * 68 - 68))
    ) -> Union[np.ndarray, np.ndarray]:
        """ Load images from directories. Directory's names should correspond
        to label of images, ex. person's name.

        :param path_to_images:
        :param path_to_classes:
        :param images_extension:

        :return: landmarks, classes
        """
        images, classes = self.get_paths_and_classes(
        	path_to_images=path_to_images,
        	path_to_classes=path_to_classes,
        	images_extension=images_extension
        )
        classes = np.array(classes)
        landmarks = np.zeros(shape=(len(images), landmarks_flatten_dimension))
        for i, image in tqdm(enumerate(images)):
            image = dlib.load_rgb_image(image)
            try:
                landmarks[i, :] = self.face_landmarks_distances(image)
            except IndexError:
                pass
        landmarks_detected = np.invert(np.all(landmarks == 0, axis=1))
        return landmarks[landmarks_detected], classes[landmarks_detected]

    def face_landmarks_distances(self, image: np.ndarray) -> np.ndarray:
        """ Return distances between face landmarks. """
        face = self.face_detector(image, 1)
        landmarks = self.face_landmarks_predictor(image, face[0])
        points = [(point.x, point.y) for point in landmarks.parts()]
        points_dists = euclidean_distances(np.array(points))
        return points_dists[np.triu_indices(points_dists.shape[0], k=1)]
