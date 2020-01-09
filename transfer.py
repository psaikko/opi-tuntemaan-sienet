import warnings as w # https://github.com/keras-team/keras/issues/8989#issuecomment-372599923
w.simplefilter(action = 'ignore', category = FutureWarning)

from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input # decode_predictions
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.utils import to_categorical

import numpy as np
import matplotlib.pyplot as plt
import json
import os.path
import random

with open("data/webscraper/luontoportti.json", "r") as f:
    data = json.loads("".join(f.readlines()))

n_classes = len(data)
class_names = [record["name_fi"] for record in data]
class_images = [[os.path.join("data/webscraper/images", image["path"]) for image in record["images"]] for record in data]
print(class_images[0])

base_model = ResNet50(weights='imagenet', include_top=False)

# https://keras.io/applications/#fine-tune-inceptionv3-on-a-new-set-of-classes
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(n_classes, activation='softmax')(x)

# learn only 
model = Model(inputs=base_model.input, outputs=predictions)
for layer in base_model.layers:
    layer.trainable = False
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy','top_k_categorical_accuracy'])

XY_data = []
X_data = None
Y_data = None
for i, images in enumerate(class_images):
    y = to_categorical(i, n_classes)
    for img_path in images:
        im = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(im)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        XY_data.append([x, y])

random.shuffle(XY_data)
XY_test = XY_data[:100]
XY_train = XY_data[100:]
X_train, Y_train = zip(*XY_train)
X_train = np.concatenate(X_train, axis=0)
Y_train = np.stack(Y_train, axis=0)

print(X_train.shape)
print(Y_train.shape)

model.fit(x=X_train, y=Y_train, batch_size=32, epochs=10, validation_split=0.2)

X_test, Y_test = zip(*XY_test)
X_test = np.concatenate(X_test, axis=0)
Y_test = np.stack(Y_test, axis=0)
model.evaluate(x=X_test, y=Y_test)

features = model.predict(x)
print(features.shape)

#plt.imshow(img)
#plt.show()