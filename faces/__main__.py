import numpy as np
import os
import time
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
    camera = cv2.VideoCapture(-1)
    while True:
        predictions = []
        for frame in range(3):
            _, image = camera.read()
            image = Videos2Frames.preprocess_frame(image,
                    rotation=None,
                    crop=dict(left=100, right=100, bottom=0, top=0),
                    resize=(256, 256))
            cv2.imshow('SpotiFaces', image)
            try:
                landmarks_dists = flt.face_landmarks_distances(image)
                prediction = logreg.predict_proba(landmarks_dists.reshape(1, 2278))
                predictions.append(['anna', 'lukasz'][np.argmax(prediction)])
            except IndexError:
                next
        print(predictions)
        if len(set(predictions)) == 1:
            if predictions[0] == 'anna':
                os.system('omxplayer -o alsa audio/anna.mp3')
            else:
                os.system('omxplayer -o alsa audio/lukasz.mp3')
            time.sleep(5)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
