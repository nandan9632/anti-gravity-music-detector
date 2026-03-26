from flask import Flask, render_template, request
import numpy as np
import librosa
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)

# ✅ LOAD MODEL & LABELS
model = load_model("instrument_model.h5")
labels = np.load("labels.npy", allow_pickle=True).item()

print("✅ Loaded Labels:", labels)


# ✅ FEATURE EXTRACTION (MATCH TRAINING)
def extract_features(file):
    try:
        y, sr = librosa.load(file, sr=22050, duration=3)

        # handle empty audio
        if len(y) == 0:
            raise ValueError("Empty audio")

        y = librosa.util.normalize(y)

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

        max_len = 130

        if mfcc.shape[1] < max_len:
            pad_width = max_len - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
        else:
            mfcc = mfcc[:, :max_len]

        return mfcc

    except Exception as e:
        print("Feature extraction error:", e)
        raise e

# ✅ MAIN ROUTE
@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""   # empty by default

    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename != "":
            filepath = "temp.wav"
            file.save(filepath)

            try:
                # ✅ Extract features
                features = extract_features(filepath)

                # ✅ IMPORTANT FIX (match training)
                features = features.flatten().reshape(1, -1)

                print("Feature shape:", features.shape)

                # ✅ Predict
                prediction = model.predict(features)

                pred_index = int(np.argmax(prediction))
                confidence = float(np.max(prediction))

                print("\n--- DEBUG ---")
                print("Prediction:", prediction)
                print("Index:", pred_index)
                print("Confidence:", confidence)

                # ✅ Confidence filter
                if confidence < 0.5:
                    result = "Unknown (Low Confidence)"
                else:
                    instrument = labels.get(pred_index, "Unknown")
                    result = f"{instrument} ({confidence*100:.2f}%)"

            except Exception as e:
                import traceback
                traceback.print_exc()
                result = "ERROR PROCESSING AUDIO"

            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)

    return render_template("index.html", result=result)


# ✅ RUN APP
if __name__ == "__main__":
    app.run(debug=True)