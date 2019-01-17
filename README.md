# Introduction

`faces` is a side-project developed during the New Year's Eve break. The main goal of the project was to create a model that recognizes the faces of the household members. The model has been implemented in `Python 3.6` and embedded on `Raspberry Pi`. `Raspberry` combined with home speakers via bluetooth welcomes home members who come to their home with their favorite music.

# Installation

To install faces, create a `conda` (or `venv`) environment with `python 3.6` and install dependencies.

```
conda create -n faces python=3.6
pip install git+https://github.com/stasulam/faces.git
```

# Starter

The model was trained on 30-second films containing the faces of the household members. Using the `train_test_split` method, remember that you should adjust the `preprocess_image` parameters to the resolution and rotation of the movie you have recorded.

```python
from faces.preprocessing import Video2Datasets

v2d = Video2Datasets(
	videos=['movie_faces_lukasz.MOV', 'movie_faces_anna.MOV'],
	people=['lukasz', 'anna'],
	train_dir='datasets/train/',
	test_dir='datasets/test/'
)
v2d.train_test_split(
	test_size=0.25,
	rotation=270, # degrees,
	crop=dict(left=420, right=420, top=0, bottom=0), # pixels
	resize=(600, 600) # pixels
)
```

Then, each frame of the recorded movie is analyzed for the detection of `68` of the key facial points.

```python
from faces.transformers import FaceLandmarksTransformer

X_train, y_train = flt.transform_from_directory(
    path_to_images='datasets/train/',
    path_to_classes=['anna', 'lukasz'],
    landmarks_flatten_dimension=int(1/2 * 68 * (68 - 1)) # upper triangular matrix without diagonal
)
X_valid, y_valid = flt.transform_from_directory(
    path_to_images='datasets/test/',
    path_to_classes=['anna', 'lukasz'],
    landmarks_flatten_dimension=int(1/2 * 68 * (68 - 1))
)
```

The classifier will be trained on a set of data composed of Euclidean distances between detected points. Due to the low computing power of `Raspberry`, it is recommended to use a logistic regression model or SVM with a linear kernel.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

logreg = LogisticRegression()
logreg.fit(X_train, y_train)
```

Even without the features selection procedure and hyperparameters tuning, the results turned out to be more than satisfying. Save the model for later predictions.

```python
import joblib

joblib.dump(logreg, 'models/logreg_68_landmarks.joblib')
```

Now you can run faces from the command line (currently in the master branch there is an implementation for macOS) with `python -m faces`.

Example usage:

```
python -m faces --landmarks models/shape_predictor_68_face_landmarks.dat
	\ --classifier logreg_68_landmarks.joblib
	\ --number_of_images 3
	\ --playlists playlists.json
	\ --people anna lukasz
```

Help for command-line arguments.

```
(faces) > $ python -m faces -h                                                                    
usage: __main__.py [-h] [--landmarks LANDMARKS] [--classifier CLASSIFIER]
                   [--number_of_images NUMBER_OF_IMAGES]
                   [--playlists PLAYLISTS] [--people PEOPLE [PEOPLE ...]]

optional arguments:
  -h, --help            show this help message and exit
  --landmarks LANDMARKS, -l LANDMARKS
                        Choose model that will be used in face landmarks
                        detection task.
  --classifier CLASSIFIER, -c CLASSIFIER
                        Choose model that will be used in face recognition
                        task.
  --number_of_images NUMBER_OF_IMAGES, -ni NUMBER_OF_IMAGES
                        Number of images which will be used in final decision.
  --playlists PLAYLISTS, -p PLAYLISTS
                        Define json with playlists.
  --people PEOPLE [PEOPLE ...], -cp PEOPLE [PEOPLE ...]
                        Define people assigned to playlists.

```

Playlists (with Spotify's `URI`):

```json
{
  "anna": [
    "spotify:artist:6o7xoNMeAUgi1SVl9rHYNk",
    "spotify:album:7gqy0a0akByODnOvBpAFCe"
  ],
  "lukasz": [
    "spotify:user:1166721861:playlist:2zCDN6nOusLnRLh4l2zPcC",
    "spotify:user:1166721861:playlist:2Z7iS1f6aqrFGeiQT3Q1AV",
    "spotify:user:1166721861:playlist:2UaHGsfSMMzYlX0X5ywlLi"
  ]
}
```

Have fun!

# What's next?

Implementation of models requiring more computing power (hosting in the cloud, request via API).

- [] Transfer learning.
- [] CNN vs. Capsule Networks.
- [] Siamese Neural Networks for One-shot Image Recognition.