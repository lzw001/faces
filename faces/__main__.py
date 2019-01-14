import numpy as np
import cv2
import joblib

from .utils import Videos2Frames
from .transformers import FaceLandmarksTransformer


if __name__ == '__main__':
	# define transformer which will be used in face landmarks prediction
	flt = FaceLandmarksTransformer('models/shape_predictor_68_face_landmarks.dat')
	# load clf
	logreg = joblib.load('models/logreg_600x600.joblib')
	# define while loop to capture image from webcam
	cv2.namedWindow('SpotiFaces')
	camera = cv2.VideoCapture(0)
	predictions = list()
	while True:
		_, image = camera.read()
		image = Videos2Frames.preprocess_frame(image,
			rotation=None,
			crop=dict(left=420, right=420, bottom=120, top=120),
			resize=(256, 256))
		cv2.imshow('SpotiFaces', image)
		try:
			landmarks_dists = flt.face_landmarks_distances(image)
			prediction = logreg.predict_proba(landmarks_dists.reshape(1, 2278))
			predictions.append(['anna', 'lukasz'][np.argmax(prediction)])
		except IndexError:
			next
		if len(predictions) == 10 and predictions.count(predictions[0]) == len(predictions):
			print(predictions[0])
			predictions = list()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	camera.release()
	cv2.destroyAllWindows()
