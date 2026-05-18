import librosa
import os

audio_path = r"E:\CCA\audio_model\dataset\real\sample.wav"

print("File Exists:", os.path.exists(audio_path))

y, sr = librosa.load(audio_path, sr=22050)

print("Audio Loaded Successfully")
print("Sample Rate:", sr)
print("Audio Shape:", y.shape)