import numpy as np
import cv2
import argparse
import joblib

from .faces_recognizer import FaceLandmarksRecognizer

parser = argparse.ArgumentParser()
parser.add_argument(
	'--landmarks', '-l',
	type=str,
	default='models/shape_predictor_68_face_landmarks.dat',
	help='Choose model that will be used in face landmarks detection task.'
)
parser.add_argument(
	'--classifier', '-c',
	type=str,
	default='models/logreg_68_landmarks.joblib',
	help='Choose model that will be used in face recognition task.'
)
args = parser.parse_args()


if __name__ == '__main__':
	# define FaceRegonizer
	flr = FaceLandmarksRecognizer(
		classifier=args.classifier,
		face_landmarks_predictor=args.landmarks
	)
	# capture image from webcam
	cv2.namedWindow('faces')
	camera = cv2.VideoCapture(0)
	while True:
		_, image = camera.read()
		try:
			person = flr.predict_class_from_frame(
				image=image,
				people=['anna', 'lukasz'],
				image_preprocess_params=dict(
					rotation=None,
					crop=dict(left=420, right=420, bottom=120, top=120),
					resize=(256, 256)
				)
			)
			print('Hello, {}'.format(person))
		except Exception as e:
			next
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	camera.release()
	cv2.destroyAllWindows()
