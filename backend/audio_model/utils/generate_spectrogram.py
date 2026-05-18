import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

audio_path = r"E:\CCA\audio_model\dataset\real\sample.wav"

output_path = r"E:\CCA\audio_model\spectrograms\real\sample.png"

# Load audio
y, sr = librosa.load(audio_path, sr=22050)

# Create Mel Spectrogram
mel_spec = librosa.feature.melspectrogram(
    y=y,
    sr=sr,
    n_mels=128
)

# Convert to decibels
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

# Plot spectrogram
plt.figure(figsize=(3, 3))

librosa.display.specshow(
    mel_spec_db,
    sr=sr,
    x_axis='time',
    y_axis='mel'
)

plt.axis('off')

# Save image
plt.savefig(
    output_path,
    bbox_inches='tight',
    pad_inches=0
)

plt.close()

print("Spectrogram Generated Successfully")
print("Saved at:", output_path)