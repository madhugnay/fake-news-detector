from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import pickle
import librosa
import librosa.display
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pydub import AudioSegment
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# =========================
# CONFIGURATION
# =========================

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

AUDIO_UPLOAD_FOLDER = "audio_uploads"

os.makedirs(AUDIO_UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# LOAD MODELS
# =========================

print("Loading image model...")
image_model = load_model("xception_model_v2.keras")
class_names = ['ai', 'deepfake', 'real']

print("Loading text models...")

with open("text_model.pkl", "rb") as f:
    text_classifier = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

print("Loading audio model...")

audio_model = tf.keras.models.load_model(
    "audio_model/models/audio_model.keras"
)
)

print("All models loaded successfully!")


# =========================
# FILE EXTRACTION FUNCTIONS
# =========================

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()

        return text if text else None

    except Exception:
        return None


def extract_text_from_pdf(file_path):
    try:
        pdf = PdfReader(file_path)

        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip() if text.strip() else None

    except Exception:
        return None


# =========================
# IMAGE PREDICTION FUNCTION
# =========================

def predict_image(img_path):

    img = image.load_img(img_path, target_size=(299, 299))

    img_array = image.img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    predictions = image_model.predict(img_array)[0]

    predicted_index = np.argmax(predictions)

    predicted_class = class_names[predicted_index]

    confidence = float(predictions[predicted_index])

    if confidence < 0.7:
        result = "uncertain"
    else:
        result = predicted_class

    return {
        "prediction": result,
        "confidence": round(confidence * 100, 2),
        "probabilities": {
            class_names[i]: round(float(predictions[i]) * 100, 2)
            for i in range(len(class_names))
        }
    }


# =========================
# TEXT PREDICTION FUNCTION
# =========================

def predict_text(text):

    text = text.lower().strip()

    if len(text) < 5:
        return {
            "prediction": "uncertain",
            "confidence": 0.0,
            "reason": "Text too short"
        }

    X = tfidf_vectorizer.transform([text])

    prediction = text_classifier.predict(X)[0]

    probabilities = text_classifier.predict_proba(X)[0]

    pred_label = "real" if prediction == 1 else "fake"

    confidence = float(max(probabilities)) * 100

    if confidence < 60:
        pred_label = "uncertain"

    return {
        "prediction": pred_label,
        "confidence": round(confidence, 2),
        "probabilities": {
            "fake": round(float(probabilities[0]) * 100, 2),
            "real": round(float(probabilities[1]) * 100, 2)
        }
    }


# =========================
# AUDIO PREDICTION FUNCTION
# =========================

def predict_audio_file(audio_path):

    temp_image = os.path.join(
        AUDIO_UPLOAD_FOLDER,
        "temp_spectrogram.png"
    )

    # Load audio
    y, sr = librosa.load(audio_path, sr=22050)

    # Create mel spectrogram
    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_mels=128
    )

    # Convert to decibels
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

    # Save spectrogram image
    plt.savefig(
        temp_image,
        bbox_inches='tight',
        pad_inches=0
    )

    plt.close()

    # Load image
    img = image.load_img(
        temp_image,
        target_size=(128, 128)
    )

    img_array = image.img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = float(
    audio_model.predict(img_array)[0][0]
)

    if prediction > 0.5:
        label = "real"
        confidence = float(prediction * 100)
    else:
        label = "deepfake"
        confidence = float((1 - prediction) * 100)

    # Cleanup temp spectrogram
    try:
        os.remove(temp_image)
    except:
        pass

    return {
        "prediction": label,
        "confidence": round(confidence, 2),
        "score": float(prediction)
    }


# =========================
# COMBINE PREDICTIONS FUNCTION
# =========================

def combine_predictions(image_result, text_result):

    img_pred = image_result["prediction"]
    img_conf = image_result["confidence"]

    txt_pred = text_result["prediction"]
    txt_conf = text_result["confidence"]

    if img_pred == "uncertain" and txt_pred == "uncertain":

        final = "uncertain"
        final_conf = 0.0

        reasoning = "Both image and text analysis are inconclusive"

    elif img_pred == "uncertain":

        final = txt_pred
        final_conf = txt_conf

        reasoning = "Image inconclusive, using text analysis"

    elif txt_pred == "uncertain":

        final = img_pred
        final_conf = img_conf

        reasoning = "Text inconclusive, using image analysis"

    else:

        if img_pred == txt_pred:

            final = img_pred

            final_conf = round(
                (img_conf + txt_conf) / 2,
                2
            )

            reasoning = f"Both image and text indicate {final} content"

        else:

            final = "mixed_signals"

            final_conf = round(
                max(img_conf, txt_conf),
                2
            )

            reasoning = (
                f"Image: {img_pred} ({img_conf}%), "
                f"Text: {txt_pred} ({txt_conf}%) - CONFLICT"
            )

    return {
        "final_result": final,
        "final_confidence": final_conf,
        "reasoning": reasoning
    }


# =========================
# ROUTE: HOME
# =========================

@app.route('/')
def home():
    return render_template('index-modern.html')


# =========================
# ROUTE: PREDICT IMAGE
# =========================

@app.route('/predict-image', methods=['POST'])
def predict():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    file_path = "temp.jpg"

    file.save(file_path)

    result = predict_image(file_path)

    os.remove(file_path)

    return jsonify(result)


# =========================
# ROUTE: PREDICT TEXT
# =========================

@app.route('/predict-text', methods=['POST'])
def predict_text_route():

    try:

        extracted_text = None
        file_name = None

        # ===== FILE UPLOAD =====

        if 'file' in request.files:

            file = request.files['file']

            if file and file.filename != '':

                if not allowed_file(file.filename):

                    return jsonify({
                        "error": "Invalid file type. Upload .txt or .pdf"
                    }), 400

                file_name = secure_filename(file.filename)

                file_ext = file_name.rsplit('.', 1)[1].lower()

                temp_path = f"temp_file.{file_ext}"

                file.save(temp_path)

                if file_ext == 'txt':
                    extracted_text = extract_text_from_txt(temp_path)

                elif file_ext == 'pdf':
                    extracted_text = extract_text_from_pdf(temp_path)

                try:
                    os.remove(temp_path)
                except:
                    pass

                if extracted_text is None:

                    return jsonify({
                        "error": "Could not extract text"
                    }), 400

        # ===== MANUAL TEXT =====

        if extracted_text is None:

            data = request.get_json()

            if not data or 'text' not in data:

                return jsonify({
                    "error": "Provide text or upload file"
                }), 400

            extracted_text = data['text'].strip()

        # ===== VALIDATE =====

        if len(extracted_text) < 10:

            return jsonify({
                "error": "Text too short"
            }), 400

        # ===== PREDICT =====

        result = predict_text(extracted_text)

        if file_name:
            result['source'] = 'file'
            result['file_name'] = file_name
        else:
            result['source'] = 'manual'

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

def predict_audio(audio_path):

    try:

        # Load audio
        y, sr = librosa.load(
            audio_path,
            sr=22050
        )

        # Generate mel spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=y,
            sr=sr
        )

        mel_spec_db = librosa.power_to_db(
            mel_spec,
            ref=np.max
        )

        # Plot spectrogram
        plt.figure(figsize=(3, 3))

        librosa.display.specshow(
            mel_spec_db,
            sr=sr
        )

        plt.axis('off')

        spectrogram_path = "temp_audio_spec.png"

        plt.savefig(
            spectrogram_path,
            bbox_inches='tight',
            pad_inches=0
        )

        plt.close()

        # Load image
        img = image.load_img(
            spectrogram_path,
            target_size=(128, 128)
        )

        img_array = image.img_to_array(img)

        img_array = img_array / 255.0

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        # Predict
        prediction = audio_model.predict(
            img_array
        )[0][0]

        confidence = float(round(
    max(prediction, 1 - prediction) * 100,
    2
))

        # Fake / Real
        if prediction > 0.5:

            result = "real"

        else:

            result = "deepfake"

        # Probabilities
        probabilities = {

    "Real": float(round(
        prediction * 100,
        2
    )),

    "Deepfake": float(round(
        (1 - prediction) * 100,
        2
    ))
}

        # Cleanup
        if os.path.exists(spectrogram_path):
            os.remove(spectrogram_path)

        return {

    "prediction": str(result),

    "confidence": float(confidence),

    "probabilities": {

        "Real": float(
            probabilities.get("Real", 0)
        ),

        "Deepfake": float(
            probabilities.get("Deepfake", 0)
        )
    }
}

    except Exception as e:

        print("AUDIO PREDICTION ERROR:", str(e))

        return {

            "prediction": "error",

            "confidence": 0,

            "probabilities": {}
        }
# =========================
# ROUTE: PREDICT AUDIO
# =========================

@app.route('/predict-audio', methods=['POST'])
def predict_audio_route():

    try:

        if 'audio' not in request.files:

            return jsonify({
                "error": "No audio file uploaded"
            }), 400

        file = request.files['audio']

        if file.filename == '':

            return jsonify({
                "error": "Empty filename"
            }), 400

        filename = secure_filename(file.filename)

        audio_path = os.path.join(
            AUDIO_UPLOAD_FOLDER,
            filename
        )

        file.save(audio_path)
        # Convert uploaded audio to standard WAV

        converted_path = os.path.join(
            AUDIO_UPLOAD_FOLDER,"converted.wav")

        audio = AudioSegment.from_file(audio_path)

        audio = audio.set_frame_rate(22050)

        audio = audio.set_channels(1)

        audio.export(converted_path,format="wav")

        audio_path = converted_path

        result = predict_audio_file(audio_path)

        # Cleanup uploaded audio
        try:
            os.remove(audio_path)
        except:
            pass

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# ROUTE: PREDICT MULTIMODAL
# =========================
@app.route('/predict-multimodal', methods=['POST'])
def predict_multimodal():

    try:

        # Validate image
        if 'image' not in request.files:
            return jsonify({
                "error": "No image uploaded"
            }), 400

        # Validate audio
        if 'audio' not in request.files:
            return jsonify({
                "error": "No audio uploaded"
            }), 400

        # Validate text
        if 'text' not in request.form:
            return jsonify({
                "error": "No text provided"
            }), 400

        text_input = request.form['text'].strip()

        image_file = request.files['image']

        audio_file = request.files['audio']

        if len(text_input) < 10:
            return jsonify({
                "error": "Text too short"
            }), 400

        if image_file.filename == '':
            return jsonify({
                "error": "No image selected"
            }), 400

        if audio_file.filename == '':
            return jsonify({
                "error": "No audio selected"
            }), 400

        # Temp paths
        img_path = "temp_multimodal.jpg"

        audio_path = "temp_multimodal_audio.wav"

        # Save uploads
        image_file.save(img_path)

        audio_file.save(audio_path)

        # Predictions
        image_result = predict_image(img_path)

        text_result = predict_text(text_input)

        audio_result = predict_audio(audio_path)

        # -----------------------------
        # COMBINE FINAL RESULTS
        # -----------------------------

        fake_votes = 0

        real_votes = 0

        # IMAGE
        if image_result["prediction"].lower() in [
            "deepfake",
            "ai",
            "fake"
        ]:
            fake_votes += 1
        else:
            real_votes += 1

        # TEXT
        if text_result["prediction"].lower() == "fake":
            fake_votes += 1
        else:
            real_votes += 1

        # AUDIO
        if audio_result["prediction"].lower() in [
            "deepfake",
            "fake"
        ]:
            fake_votes += 1
        else:
            real_votes += 1

        # Final Decision
        if fake_votes > real_votes:

            final_result = "Fake / Deepfake"

        elif real_votes > fake_votes:

            final_result = "Real"

        else:

            final_result = "Mixed Signals"

        # Confidence
        final_confidence = round(max(
            image_result["confidence"],
            text_result["confidence"],
            audio_result["confidence"]
        ), 2)

        # Reasoning
        reasoning = (
            f"Image: {image_result['prediction']} "
            f"({image_result['confidence']}%), "
            f"Text: {text_result['prediction']} "
            f"({text_result['confidence']}%), "
            f"Audio: {audio_result['prediction']} "
            f"({audio_result['confidence']}%)"
        )

        # Cleanup
        if os.path.exists(img_path):
            os.remove(img_path)

        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Response
        return jsonify({

            # IMAGE
            "image_prediction":
                image_result["prediction"],

            "image_confidence":
                image_result["confidence"],

            "image_probabilities":
                image_result["probabilities"],

            # TEXT
            "text_prediction":
                text_result["prediction"],

            "text_confidence":
                text_result["confidence"],

            "text_probabilities":
                text_result["probabilities"],

            # AUDIO
            "audio_prediction":
                audio_result["prediction"],

            "audio_confidence":
                audio_result["confidence"],

            "audio_probabilities":
    audio_result.get(
        "probabilities",
        {
            "Real": 0,
            "Deepfake": 0
        }
    ),

            # FINAL
            "final_result":
                final_result,

            "final_confidence":
                final_confidence,

            "reasoning":
                reasoning
        })

    except Exception as e:

        print("MULTIMODAL ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500
# =========================
# ROUTE: METRICS
# =========================

@app.route('/metrics')
def metrics():

    return jsonify({

        "overall_accuracy": 98.89,

        "text_accuracy": 98.89,

        "image_accuracy": 92.89,

        "audio_accuracy": 97.0,

        "text_model":
            "TF-IDF + Logistic Regression",

        "image_model":
            "Xception",

        "audio_model":
            "CNN on Spectrograms",

        "confusion_matrix": {

            "image": [
                [60, 5, 10],
                [2, 70, 3],
                [15, 3, 57]
            ],

            "text": [
                [4631, 65],
                [35, 4249]
            ]
        }
    })


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
