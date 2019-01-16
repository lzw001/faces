import numpy as np
import cv2
import dlib
import joblib

from typing import List
from .transformers import FaceLandmarksTransformer


class FaceLandmarksRecognizer(FaceLandmarksTransformer):

    def __init__(self, classifier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classifier = joblib.load(classifier)

    def predict_class_from_frame(
        self,
        image: np.ndarray,
        people: list = ['anna', 'lukasz'],
        image_preprocess_params: dict = None
    ) -> list:
        """ Predict class from single frame. This method should be used
        in environments with highly constrained computational power, ex. RaspberryPi.

        :param image:
        :param people:
        :param image_preprocess_params:

        :return: people
        """
        if image_preprocess_params:
            image = self.preprocess_image(image, **image_preprocess_params)
        try:
            landmarks_dists = self.face_landmarks_distances(image)
            prediction = self.classifier.predict_proba(
                landmarks_dists.reshape(1, -1))
            return people[np.argmax(prediction)]
        except IndexError as e:
            print(e.args + ('face not found.',))

    def predict_class_from_frames(
        self,
        images: List[np.ndarray],
        people: list = ['anna', 'lukasz'],
        image_preprocess_params: dict = None
    ) -> list:
        """ Predict classes from consecutives frames. This method could be safer
        (but slower) than predict_class_from_frame. It returns the class after prediction
        made on every frame.

        :param images:
        :param people:
        :param image_preprocess_params:
        """
        predictions = []
        for image in images:
            prediction = self.predict_class_from_frame(
                image,
                people=people,
                image_preprocess_params=image_preprocess_params
            )
            predictions.append(prediction)
        predictions_on_every_frame = len(predictions) == len(images)
        predictions_all_equal = predictions.count(predictions[0]) == len(predictions)
        if predictions_on_every_frame and predictions_all_equal:
            return predictions[0]
        else:
            return None
