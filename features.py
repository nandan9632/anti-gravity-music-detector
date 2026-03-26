import librosa
import numpy as np

def extract_features(file):
    y, sr = librosa.load(file, duration=3)

    # normalize
    y = librosa.util.normalize(y)

    # MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

    # CHROMA
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)

    # SPECTRAL
    spec = librosa.feature.spectral_contrast(y=y, sr=sr)

    # take mean
    mfcc = np.mean(mfcc.T, axis=0)
    chroma = np.mean(chroma.T, axis=0)
    spec = np.mean(spec.T, axis=0)

    return np.hstack((mfcc, chroma, spec))