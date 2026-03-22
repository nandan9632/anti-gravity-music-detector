import os
import numpy as np
from features import extract_features
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

DATASET_PATH = "dataset"

X, y = [], []
labels = {}
label_index = 0

for instrument in os.listdir(DATASET_PATH):
    labels[label_index] = instrument
    folder = os.path.join(DATASET_PATH, instrument)

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        X.append(extract_features(file_path))
        y.append(label_index)

    label_index += 1

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    Dense(128, activation='relu', input_shape=(40,)),
    Dense(64, activation='relu'),
    Dense(len(labels), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10)

model.save("instrument_model.h5")
np.save("labels.npy", labels)

print("Model trained!")