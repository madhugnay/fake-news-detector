from tensorflow.keras.models import load_model

print("Loading old model...")
model = load_model("backend/xception_model_v2.keras")

print("Saving Render compatible model...")
model.save("backend/xception_render.h5")

print("Done")