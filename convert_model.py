import tensorflow as tf
from tensorflow.keras.models import load_model

print("Loading model...")

model = load_model(
    "backend/xception_model_v2.keras",
    compile=False
)

print("Saving clean model...")

tf.keras.models.save_model(
    model,
    "backend/xception_render.h5",
    save_format="h5",
    include_optimizer=False
)

print("Done")