from tensorflow.keras.models import load_model

print("Loading original model...")

model = load_model(
    "backend/xception_model_v2.keras",
    compile=False
)

print("Saving weights only...")

model.save_weights(
    "backend/xception_weights.weights.h5"
)

print("Done")