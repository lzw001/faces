import os
import cv2
import time

from .faces_recognizer import FacesRecognizer
from .player import Player


if __name__ == '__main__':
	# define recognizer
	recognizer = FacesRecognizer(
		faces_shape_predictor='models/shape_predictor_68_face_landmarks.dat',
		faces_classifier='models/faces_logreg.joblib',
		faces_names=['anna', 'lukasz']
	)
	# define Player
	player = Player()
	# detect faces with webcam
	camera = cv2.VideoCapture(0)
	cv2.namedWindow('SpotiFaces')
	while True:
		ret, image = camera.read()
		try:
			people = recognizer.recognize(image)
			if len(people.keys()) == 1:
				if list(people.keys()) == ['anna']:
					os.system('bash spotify.sh play "z imbirem"')
					time.sleep(3)
				else:
					os.system('bash spotify.sh play uri spotify:user:1166721861:playlist:2zCDN6nOusLnRLh4l2zPcC')
					time.sleep(3)
		except Exception:
			next
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	camera.release()
	cv2.destroyAllWindows()
