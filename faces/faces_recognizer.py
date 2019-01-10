import numpy as np
import cv2
import dlib
import joblib

from sklearn.metrics import euclidean_distances


class FacesRecognizer(object):
    """FacesRecognizer implements methods used in face recognition problem."""
    def __init__(
        self,
        faces_shape_predictor: str,
        faces_classifier: str,
        faces_names: list = ['anna', 'lukasz']
    ) -> None:

        self.faces_shape_predictor = dlib.shape_predictor(faces_shape_predictor)
        self.faces_classifier = joblib.load(faces_classifier)
        self.faces_names = faces_names

    def recognize(self, image: np.ndarray) -> dict:
        """
        """
        faces = dlib.get_frontal_face_detector()(image, 1)
        recognized_people = dict()
        for face in faces:
            face_landmarks = self.faces_shape_predictor(image, face)
            face_landmarks_points = [(point.x, point.y)
                for point in face_landmarks.parts()]
            face_landmarks_dists = euclidean_distances(
                np.array(face_landmarks_points)).reshape(1, -1)
            clf_proba = self.faces_classifier.predict_proba(face_landmarks_dists)
            person = self.faces_names[np.argmax(clf_proba)]
            recognized_people[person] = dict(
                top=face.top(),
                bottom=face.bottom(),
                left=face.left(),
                right=face.right()
            )
        return recognized_people
