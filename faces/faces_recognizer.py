import numpy as np
import cv2
import dlib
import joblib

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
		"""
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
