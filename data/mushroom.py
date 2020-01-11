import numpy as np
import json
from os import path
import random
from keras.preprocessing import image
from keras.utils import to_categorical

def load_data(testset_size=100):
    with open(path.join(path.dirname(path.realpath(__file__)),"aggregated.json"), "r") as f:
        data = json.loads("".join(f.readlines()))

    n_classes = len(data)
    class_names = [record["name_fi"] for record in data]
    class_images = [record["images"] for record in data]

    XY_data = []
    for i, images in enumerate(class_images):
        y = to_categorical(i, n_classes)
        for img_path in images:
            im = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(im)
            x = np.expand_dims(x, axis=0)
            XY_data.append([x, y])

    random.seed(1)
    random.shuffle(XY_data)
    XY_test = XY_data[:testset_size]
    XY_train = XY_data[testset_size:]
    X_train, Y_train = zip(*XY_train)
    X_train = np.concatenate(X_train, axis=0)
    Y_train = np.stack(Y_train, axis=0)

    X_test, Y_test = zip(*XY_test)
    X_test = np.concatenate(X_test, axis=0)
    Y_test = np.stack(Y_test, axis=0)
    
    return (X_train, Y_train), (X_test, Y_test), class_names

    