import warnings as w # https://github.com/keras-team/keras/issues/8989#issuecomment-372599923
w.simplefilter(action = 'ignore', category = FutureWarning)

from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.preprocessing.image import ImageDataGenerator
from data.mushroom import load_data
import matplotlib.pyplot as plt
import numpy as np

(X_train, Y_train), (X_test, Y_test), class_names = load_data()

datagen = ImageDataGenerator(rotation_range=45, 
    brightness_range=(0.5,1.5), 
    height_shift_range=0.3,
    width_shift_range=0.3,
    horizontal_flip=True,
    fill_mode="reflect",
    zoom_range=(0.5,1.5),
    validation_split=0.1,
    preprocessing_function=preprocess_input)

# for X_batch, y_batch in datagen.flow(X_train, Y_train, batch_size=9):
#     for i in range(0, 9):
#         plt.subplot(331 + i)
#         # normalize for display
#         vmin, vmax = np.min(X_batch[i]), np.max(X_batch[i])
#         plt.imshow((X_batch[i] - vmin) / (vmax - vmin))
#     plt.show()
#     break

base_model = ResNet50(weights='imagenet', include_top=False)

# https://keras.io/applications/#fine-tune-inceptionv3-on-a-new-set-of-classes
x = base_model.output
x = GlobalAveragePooling2D()(x)
#x = Dense(1024, activation='relu')(x)
predictions = Dense(len(class_names), activation='softmax')(x)

# Learn only weights for newly added layers
model = Model(inputs=base_model.input, outputs=predictions)
for layer in base_model.layers:
    layer.trainable = False
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy','top_k_categorical_accuracy'])

batchsize = 100
model.fit_generator(datagen.flow(X_train, Y_train, batch_size=batchsize, subset='training'),
    steps_per_epoch=(len(X_train) / batchsize), 
    epochs=10,
    validation_data=datagen.flow(X_train, Y_train, batch_size=batchsize, subset='validation'))

scores = model.evaluate_generator(datagen.flow(X_test, Y_test))
print("Testset scores")
for (name, score) in zip(["Loss","Accuracy","Top 5"], scores):
    print("  %s: %.2f" % (name, score))

with open("mushroom-resnet.json", "w") as json_file:
    json_file.write(model.to_json())
model.save_weights("mushroom-resnet.h5")
