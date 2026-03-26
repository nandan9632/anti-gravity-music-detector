import os
import numpy as np
from features import extract_features
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

DATASET_PATH = "dataset"

X, y = [], []
labels = {}
label_index = 0

print("Loading dataset...")

# ✅ LOAD DATASET
for instrument in os.listdir(DATASET_PATH):

    folder = os.path.join(DATASET_PATH, instrument)

    # skip non-folders
    if not os.path.isdir(folder):
        continue

    labels[label_index] = instrument
    print(f"Label {label_index}: {instrument}")

    count = 0

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        try:
            features = extract_features(file_path)
            X.append(features)
            y.append(label_index)
            count += 1
        except Exception as e:
            print("❌ Error loading:", file)

    print(f"{instrument}: {count} files loaded")

    label_index += 1


# ✅ CONVERT TO NUMPY
X = np.array(X)
y = np.array(y)

print("Dataset shape:", X.shape)

# ✅ CHECK BALANCE
print("Class distribution:", np.bincount(y))


# ✅ FLATTEN FEATURES (IMPORTANT 🔥)
X = X.reshape(X.shape[0], -1)


# ✅ SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ✅ MODEL
model = Sequential([
    Dense(256, activation='relu', input_shape=(X.shape[1],)),
    Dropout(0.3),

    Dense(128, activation='relu'),
    Dropout(0.3),

    Dense(64, activation='relu'),

    Dense(len(labels), activation='softmax')
])


# ✅ COMPILE
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)


# ✅ TRAIN
model.fit(
    X_train,
    y_train,
    epochs=60,
    batch_size=32,
    validation_data=(X_test, y_test)
)


# ✅ SAVE
model.save("instrument_model.h5")
np.save("labels.npy", labels)

print("✅ Model trained successfully!")
print("Labels:", labels)