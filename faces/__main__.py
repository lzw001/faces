import os
import codecs
import json
import argparse
import random
import time
import cv2

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
parser.add_argument(
    '--number_of_images', '-ni',
    type=int,
    default=3,
    help='Number of images which will be used in final decision.'
)
parser.add_argument(
    '--playlists', '-p',
    type=str,
    default='playlists.json',
    help='Define json with playlists.'
)
parser.add_argument(
    '--people', '-cp',
    type=str,
    nargs='+',
    default=['anna', 'lukasz'],
    help='Define people assigned to playlists.'
)
args = parser.parse_args()

with codecs.open(args.playlists, encoding='utf-8') as playlists:
    playlists = json.load(playlists)

if __name__ == '__main__':
    # define FaceRegonizer
    flr = FaceLandmarksRecognizer(
        classifier=args.classifier,
        face_landmarks_predictor=args.landmarks
    )
    # capture image from webcam
    cv2.namedWindow('faces')
    camera, images = cv2.VideoCapture(0), []
    while True:
        _, image = camera.read()
        images.append(image)
        if len(images) == args.number_of_images:
            person = flr.predict_class_from_frames(
                images=images,
                people=args.people,
                image_preprocess_params=dict(
                    rotation=None,
                    crop=dict(left=420, right=420, bottom=120, top=120),
                    resize=(256, 256)
                )
            )
            if person:
                print('Hello, {}'.format(person))
                cmd = 'bash shpotify.sh play uri {}'.format(
                    random.choice(playlists[person]))
                os.system(cmd)
                time.sleep(5)
            # clear images list for next iteration of while loop
            images = []
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
