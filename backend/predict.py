import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# =========================
# LOAD MODEL
# =========================
model = load_model("xception_model_v2.keras")

# Class labels
class_names = ['ai', 'deepfake', 'real']

# =========================
# PREDICTION FUNCTION
# =========================
def predict_image(img_path):
    # Check if file exists
    if not os.path.exists(img_path):
        print(f"❌ Error: File '{img_path}' not found!")
        return

    # Load image
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)[0]

    predicted_index = np.argmax(predictions)
    predicted_class = class_names[predicted_index]
    confidence = predictions[predicted_index]

    # =========================
    # SMART OUTPUT LOGIC
    # =========================
    print("\n🔍 Prediction Result:")

    if confidence < 0.7:
        print("⚠️ Uncertain Prediction")
        print(f"Most Likely: {predicted_class.upper()} ({confidence*100:.2f}%)")
    else:
        print(f"Class: {predicted_class.upper()}")
        print(f"Confidence: {confidence*100:.2f}%")

    # Show all probabilities
    print("\n📊 Detailed Probabilities:")
    for i, prob in enumerate(predictions):
        print(f"{class_names[i]}: {prob*100:.2f}%")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    img_path = input("Enter image path: ")   # 👈 user input
    predict_image(img_path)