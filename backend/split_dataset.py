import os
import random
import shutil

# Source dataset path
base_dir = "datasets"

# Destination base folder
output_dir = "dataset"

classes = ["real", "ai", "deepfake"]

for cls in classes:
    src = os.path.join(base_dir, cls)

    # Create destination folders
    train_dir = os.path.join(output_dir, "train", cls)
    val_dir = os.path.join(output_dir, "val", cls)
    test_dir = os.path.join(output_dir, "test", cls)

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Get all images
    files = [f for f in os.listdir(src) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    random.shuffle(files)

    # Split ratios
    train_split = int(0.7 * len(files))
    val_split = int(0.85 * len(files))

    train_files = files[:train_split]
    val_files = files[train_split:val_split]
    test_files = files[val_split:]

    # Copy files
    for f in train_files:
        shutil.copy(os.path.join(src, f), os.path.join(train_dir, f))

    for f in val_files:
        shutil.copy(os.path.join(src, f), os.path.join(val_dir, f))

    for f in test_files:
        shutil.copy(os.path.join(src, f), os.path.join(test_dir, f))

    print(f"✅ {cls} done: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test")