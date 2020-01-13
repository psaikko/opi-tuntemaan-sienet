from keras.models import model_from_json
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image
from os import path
import matplotlib.pyplot as plt
import numpy as np
import sys
import json

with open('mushroom-resnet.json', 'r') as f:
    model_json = f.read()
model = model_from_json(model_json)
model.load_weights("mushroom-resnet.h5")

filepaths = sys.argv[1:]
X_predict = []

for img_path in filepaths:
    im = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(im)
    x = np.expand_dims(x, axis=0)
    X_predict.append(preprocess_input(x))

X_predict = np.concatenate(X_predict, axis=0)

with open(path.join(path.dirname(path.realpath(__file__)),"data/aggregated.json"), "r") as f:
    data = json.loads("".join(f.readlines()))
class_names = [record["name_fi"] for record in data]

for j, Y_pred in enumerate(model.predict(X_predict)):
    class_vals = enumerate(Y_pred)
    class_vals = sorted(class_vals, key=lambda p:p[1], reverse=True)
    print("Top 5:")
    for i, v in class_vals[:5]:
        print("  %s %.2f" % (class_names[i], v))
    plt.imshow(image.load_img(filepaths[j], target_size=(224, 224)))
    plt.show()
