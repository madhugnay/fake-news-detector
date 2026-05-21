from tensorflow.keras.models import load_model

print("Loading original model...")

model = load_model(
    "backend/xception_model_v2.keras",
    compile=False
)

print("Saving Render model...")

model.save(
    "backend/xception_render.keras"
)

print("Done")