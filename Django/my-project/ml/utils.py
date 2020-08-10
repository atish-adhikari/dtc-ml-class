import numpy as np
import os
import pickle
import cv2
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.applications.inception_resnet_v2 import decode_predictions


this_dir = os.path.dirname(os.path.abspath(__file__)) 
pipeline_file = os.path.join(this_dir, "saved_models", "ml_pipeline.pkl")
f = open(pipeline_file, "rb")
model1 = pickle.load(f)
f.close()

cascade_path = os.path.join(this_dir, "saved_models", 'haarcascade_frontalface_alt2.xml')
image_size = 160

model_path = os.path.join(this_dir, "saved_models", 'facenet_keras.h5')
model = load_model(model_path)


get_model = lambda : model1

def get_cnn():
    return (InceptionResNetV2(weights="imagenet"), decode_predictions)

def prewhiten(x):
    if x.ndim == 4:
        axis = (1, 2, 3)
        size = x[0].size
    elif x.ndim == 3:
        axis = (0, 1, 2)
        size = x.size
    else:
        raise ValueError('Dimension should be 3 or 4')

    mean = np.mean(x, axis=axis, keepdims=True)
    std = np.std(x, axis=axis, keepdims=True)
    std_adj = np.maximum(std, 1.0/np.sqrt(size))
    y = (x - mean) / std_adj
    return y

def l2_normalize(x, axis=-1, epsilon=1e-10):
    output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
    return output

def load_and_align_images(filepath, margin):
    cascade = cv2.CascadeClassifier(cascade_path)
    
    aligned_images = []

    img = filepath
    img = np.array(img)

    faces = cascade.detectMultiScale(img,
                                        scaleFactor=1.1,
                                        minNeighbors=3)
    (x, y, w, h) = faces[0]
    cropped = img[y-margin//2:y+h+margin//2,
                    x-margin//2:x+w+margin//2, :]
    aligned = cv2.resize(cropped, (image_size, image_size))
    aligned_images.append(aligned)
            
    return np.array(aligned_images)

def calc_embs(filepaths, margin=10, batch_size=1):
    aligned_images = prewhiten(load_and_align_images(filepaths, margin))
    pd = []
    for start in range(0, len(aligned_images), batch_size):
        pd.append(model.predict_on_batch(aligned_images[start:start+batch_size]))
    embs = l2_normalize(np.concatenate(pd))

    return embs

def infer(le, clf, filepaths):
    embs = calc_embs(filepaths)
    pred = le.inverse_transform(clf.predict(embs))
    return pred

f = open(os.path.join(this_dir, "saved_models", "le.pkl"), "rb")
le = pickle.load(f)
f.close()

f = open(os.path.join(this_dir, "saved_models", "clf.pkl"), "rb")
clf = pickle.load(f)
f.close()

get_le_clf = lambda: (le, clf)