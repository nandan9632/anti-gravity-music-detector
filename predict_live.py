import sounddevice as sd
import numpy as np
import librosa
from tensorflow.keras.models import load_model
from ui import show_floating_text

model = load_model("instrument_model.h5")
labels = np.load("labels.npy", allow_pickle=True).item()

def record_audio(duration=3, fs=22050):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return audio.flatten()

def extract_features_live(audio, sr=22050):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

while True:
    audio = record_audio()
    features = extract_features_live(audio).reshape(1, -1)

    prediction = model.predict(features)
    instrument = labels[np.argmax(prediction)]

    print("Detected:", instrument)
    show_floating_text(instrument)