import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# =========================
# PATHS
# =========================
train_dir = "dataset/train"
val_dir = "dataset/val"
test_dir = "dataset/test"

# =========================
# IMAGE SETTINGS
# =========================
IMG_SIZE = (299, 299)
BATCH_SIZE = 32

# =========================
# DATA AUGMENTATION (IMPROVED)
# =========================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    rotation_range=20,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2]
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

test_generator = val_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

print("Classes:", train_generator.class_indices)

# =========================
# LOAD XCEPTION
# =========================
base_model = Xception(
    weights='imagenet',
    include_top=False,
    input_shape=(299, 299, 3)
)

# Freeze all layers first
for layer in base_model.layers:
    layer.trainable = False

# =========================
# ADD CUSTOM LAYERS (IMPROVED)
# =========================
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(1024, activation='relu')(x)
x = layers.Dropout(0.5)(x)  # 🔥 reduces overfitting
output = layers.Dense(3, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)

# =========================
# COMPILE (LOW LR)
# =========================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# =========================
# TRAIN FIRST PHASE
# =========================
print("🔹 Training top layers...")
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=5
)

# =========================
# FINE-TUNING (UNFREEZE LAST LAYERS)
# =========================
for layer in base_model.layers[-30:]:
    layer.trainable = True

# Recompile with lower LR
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# =========================
# TRAIN SECOND PHASE
# =========================
print("🔹 Fine-tuning model...")
history_fine = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

# =========================
# EVALUATE
# =========================
loss, acc = model.evaluate(test_generator)
print(f"Test Accuracy: {acc * 100:.2f}%")

# =========================
# SAVE MODEL
# =========================
model.save("xception_model_v2.keras")
print("✅ Improved model saved!")