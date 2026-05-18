import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

# =========================
# PATHS
# =========================

MODEL_PATH = r"E:\CCA\audio_model\models\audio_model.keras"

AUDIO_PATH = r"E:\CCA\audio_model\test_audio_fake.wav"

TEMP_SPECTROGRAM = r"E:\CCA\audio_model\temp1.png"

# =========================
# LOAD MODEL
# =========================

model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# LOAD AUDIO
# =========================

y, sr = librosa.load(AUDIO_PATH, sr=22050)

# =========================
# CREATE SPECTROGRAM
# =========================

mel_spec = librosa.feature.melspectrogram(
    y=y,
    sr=sr,
    n_mels=128
)

mel_spec_db = librosa.power_to_db(
    mel_spec,
    ref=np.max
)

plt.figure(figsize=(3,3))

librosa.display.specshow(
    mel_spec_db,
    sr=sr
)

plt.axis('off')

plt.savefig(
    TEMP_SPECTROGRAM,
    bbox_inches='tight',
    pad_inches=0
)

plt.close()

# =========================
# PREPROCESS IMAGE
# =========================

img = image.load_img(
    TEMP_SPECTROGRAM,
    target_size=(128,128)
)

img_array = image.img_to_array(img)

img_array = img_array / 255.0

img_array = np.expand_dims(img_array, axis=0)

# =========================
# PREDICTION
# =========================

prediction = model.predict(img_array)[0][0]

print("\nPrediction Score:", prediction)

if prediction > 0.5:
    print("Prediction: REAL AUDIO")
else:
    print("Prediction: FAKE / DEEPFAKE AUDIO")
