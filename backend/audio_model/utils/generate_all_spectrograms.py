import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Dataset paths
DATASET_PATH = r"E:\CCA\audio_model\dataset"
SPECTROGRAM_PATH = r"E:\CCA\audio_model\spectrograms"

# Classes
classes = ["real", "fake"]

# Generate spectrograms
for label in classes:

    audio_folder = os.path.join(DATASET_PATH, label)
    output_folder = os.path.join(SPECTROGRAM_PATH, label)

    os.makedirs(output_folder, exist_ok=True)

    files = os.listdir(audio_folder)

    print(f"\nProcessing {label} files...")

    for index, file_name in enumerate(files):

        try:
            audio_path = os.path.join(audio_folder, file_name)

            # Load audio
            y, sr = librosa.load(audio_path, sr=22050)

            # Create mel spectrogram
            mel_spec = librosa.feature.melspectrogram(
                y=y,
                sr=sr,
                n_mels=128
            )

            # Convert to dB
            mel_spec_db = librosa.power_to_db(
                mel_spec,
                ref=np.max
            )

            # Plot
            plt.figure(figsize=(3, 3))

            librosa.display.specshow(
                mel_spec_db,
                sr=sr
            )

            plt.axis('off')

            # Save image
            save_path = os.path.join(
                output_folder,
                file_name.replace(".wav", ".png")
            )

            plt.savefig(
                save_path,
                bbox_inches='tight',
                pad_inches=0
            )

            plt.close()

            print(f"{index+1}/{len(files)} done")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

print("\nAll spectrograms generated successfully!")