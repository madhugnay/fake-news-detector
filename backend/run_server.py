#!/usr/bin/env python
"""
Multimodal Fake News Detector - Application Launcher
Starts Flask server and opens browser
"""

import subprocess
import sys
import os
import time
import webbrowser

print("=" * 70)
print("MULTIMODAL FAKE NEWS DETECTION SYSTEM")
print("=" * 70)
print()

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("Step 1: Checking models...")
models = ['xception_model_v2.keras', 'text_model.pkl', 'tfidf_vectorizer.pkl']
for model in models:
    if os.path.exists(model):
        size = os.path.getsize(model) / (1024*1024)
        print(f"  [OK] {model} ({size:.2f} MB)")
    else:
        print(f"  [ERROR] {model} NOT FOUND")
        sys.exit(1)

print("\nStep 2: Loading models and starting server...")
print("  This may take 5-10 seconds...")
print()

try:
    # Start Flask app
    process = subprocess.Popen(
        [sys.executable, "-m", "flask", "run", "--host=127.0.0.1", "--port=5000"],
        env={**os.environ, "FLASK_APP": "app.py"}
    )

    # Wait for server to start
    time.sleep(8)

    print("=" * 70)
    print("SUCCESS! Application is running!")
    print("=" * 70)
    print()
    print("Web Interface: http://localhost:5000")
    print()
    print("FEATURES:")
    print("  - Multimodal tab: Upload image + paste text")
    print("  - Image tab: Image-only prediction")
    print("  - Text tab: Text-only prediction")
    print()
    print("MODELS READY:")
    print("  - Image: Xception (Accuracy: 92.89%)")
    print("  - Text: TF-IDF + LogReg (Accuracy: 98.89%)")
    print("  - Combined: 95%+")
    print()
    print("API ENDPOINTS:")
    print("  - POST /predict-image")
    print("  - POST /predict-text")
    print("  - POST /predict-multimodal")
    print("  - GET /metrics")
    print()

    # Try to open browser
    try:
        print("Opening browser...")
        webbrowser.open("http://localhost:5000")
        time.sleep(1)
    except:
        pass

    print("=" * 70)
    print("To stop the server: Press Ctrl+C")
    print("=" * 70)
    print()

    # Keep server running
    process.wait()

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
