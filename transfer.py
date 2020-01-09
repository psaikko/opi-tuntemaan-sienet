import warnings as w # https://github.com/keras-team/keras/issues/8989#issuecomment-372599923
w.simplefilter(action = 'ignore', category = FutureWarning)

from keras.applications.resnet50 import ResNet50
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D

from data.mushroom import load_data

(X_train, Y_train), (X_test, Y_test), class_names = load_data()

base_model = ResNet50(weights='imagenet', include_top=False)

# https://keras.io/applications/#fine-tune-inceptionv3-on-a-new-set-of-classes
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(len(class_names), activation='softmax')(x)

# learn only 
model = Model(inputs=base_model.input, outputs=predictions)
for layer in base_model.layers:
    layer.trainable = False
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy','top_k_categorical_accuracy'])

model.fit(x=X_train, y=Y_train, batch_size=32, epochs=10, validation_split=0.2)
model.evaluate(x=X_test, y=Y_test)
