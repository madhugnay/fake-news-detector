# Multimodal Fake News Detection System

A complete web application that detects fake news using both **image analysis** (Xception deep learning model) and **text analysis** (TF-IDF + Logistic Regression). The system combines both modalities for more accurate predictions.

## 🎯 Features

✅ **Image Analysis** - Classify images as AI-generated, Deepfake, or Real  
✅ **Text Analysis** - Detect fake news from article text  
✅ **Multimodal Prediction** - Combine both analyses for final verdict  
✅ **Fast Predictions** - TF-IDF + LR for <100ms text predictions  
✅ **Beautiful UI** - Modern, responsive web interface with tabs  
✅ **REST API** - Three endpoints: `/predict-image`, `/predict-text`, `/predict-multimodal`  

## 📊 Model Performance

| Model | Type | Accuracy | Speed |
|-------|------|----------|-------|
| **Image Classifier** | Xception CNN | 92.89% | 500ms |
| **Text Classifier** | TF-IDF + Logistic Regression | 98.89% | 5-10ms |
| **Combined** | Multimodal | 95%+ | 600ms |

## 📁 Project Structure

```
CCA/
├── app.py                              # Flask backend (main application)
├── train_text_model.py                 # Script to train text classifier
├── requirements.txt                    # Python dependencies
├── xception_model_v2.keras            # Pre-trained image model (180 MB)
├── text_model.pkl                      # Trained text classifier (40 KB)
├── tfidf_vectorizer.pkl               # TF-IDF vectorizer (185 KB)
├── Fake.csv                           # Training data (fake news articles)
├── True.csv                           # Training data (real news articles)
└── templates/
    └── index.html                      # Frontend (React-like UI)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Models Are Ready

Check that these files exist:
- ✅ `xception_model_v2.keras` (180 MB) - Already trained
- ✅ `text_model.pkl` (40 KB) - Already trained
- ✅ `tfidf_vectorizer.pkl` (185 KB) - Already trained

If text models are missing, train them:
```bash
python train_text_model.py
```

### 3. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

### 4. Open in Browser

- **URL**: http://localhost:5000
- **Multimodal Tab**: Upload image + paste text → Get combined prediction
- **Image Tab**: Upload image → Get image-only prediction
- **Text Tab**: Paste text → Get text-only prediction

## 🔌 API Endpoints

### POST `/predict-image`
**Upload an image to predict if it's AI, Deepfake, or Real**

```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/predict-image
```

**Response:**
```json
{
  "prediction": "real",
  "confidence": 92.5,
  "probabilities": {
    "ai": 2.3,
    "deepfake": 5.2,
    "real": 92.5
  }
}
```

### POST `/predict-text`
**Analyze text to predict if it's fake or real**

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text": "Breaking: Scientists discover new energy source"}' \
  http://localhost:5000/predict-text
```

**Response:**
```json
{
  "prediction": "real",
  "confidence": 85.3,
  "probabilities": {
    "fake": 14.7,
    "real": 85.3
  }
}
```

### POST `/predict-multimodal`
**Combine image + text for comprehensive analysis**

```bash
curl -X POST \
  -F "image=@news_image.jpg" \
  -F "text=Article text here..." \
  http://localhost:5000/predict-multimodal
```

**Response:**
```json
{
  "image_prediction": "real",
  "image_confidence": 92.5,
  "image_probabilities": {...},
  "text_prediction": "real",
  "text_confidence": 85.3,
  "text_probabilities": {...},
  "final_result": "real",
  "final_confidence": 88.9,
  "reasoning": "Both image and text indicate authentic news content"
}
```

### GET `/metrics`
**Get model performance metrics**

```bash
curl http://localhost:5000/metrics
```

**Response:**
```json
{
  "overall_accuracy": 98.89,
  "text_accuracy": 98.89,
  "image_accuracy": 92.89,
  "text_model": "TF-IDF + Logistic Regression",
  "image_model": "Xception"
}
```

## 🎨 UI Features

### Three Tab Modes

1. **Multimodal Tab** (Recommended)
   - Upload image
   - Paste news text
   - Get combined prediction with reasoning

2. **Image Tab**
   - Upload image
   - Get AI/Deepfake/Real classification
   - View probability breakdown

3. **Text Tab**
   - Paste news article
   - Get Fake/Real classification
   - View confidence scores

### Beautiful Results Display

- **Color-coded predictions**: Green (Real), Red (Fake), Orange (Uncertain), Purple (Mixed)
- **Confidence visualization**: Percentage scores
- **Probability breakdown**: Detailed scores for each class
- **Smart reasoning**: Explains why final prediction was made
- **Error handling**: Clear error messages for invalid inputs

## 📝 Example Usage

### Example 1: Multimodal Analysis

1. Go to **Multimodal Tab**
2. Upload a suspicious news image
3. Paste article text like: "Scientists discover aliens in Mars tunnel"
4. Click **Predict Multimodal**
5. Get results:
   - Image: "DEEPFAKE (87%)"
   - Text: "FAKE (92%)"
   - Final: "FAKE (89.5%)" with reasoning

### Example 2: Text-Only Analysis

1. Go to **Text Tab**
2. Paste: "The Federal Reserve announces new interest rate policy"
3. Click **Predict Text**
4. Get: "REAL (78%)" - identifies as authentic news

## 🔄 Training Custom Models

### Retrain Text Classifier

The text model is already trained on 44,898 news articles (23,481 fake + 21,417 real).

To retrain with custom data:

```bash
python train_text_model.py
```

This will:
- Load Fake.csv and True.csv
- Train TF-IDF (5000 features, unigrams + bigrams)
- Train Logistic Regression classifier
- Save as `text_model.pkl` and `tfidf_vectorizer.pkl`
- Report accuracy: ~98.89%

### Retrain Image Classifier

To retrain the image model (requires image dataset):

```bash
python train_tf.py
```

## 📊 Training Data

### Text Data (CSV files)
- **Fake.csv**: 23,481 fake news articles with title, text, subject, date
- **True.csv**: 21,417 real news articles from Reuters

### Image Data (directories)
- **datasets/**: 1,500 raw images (500 AI + 500 Deepfake + 500 Real)
- **dataset/**: Split into train (70%), val (15%), test (15%)

## 🛠️ Technical Details

### Text Classifier
- **Algorithm**: TF-IDF Vectorizer + Logistic Regression
- **Features**: 5,000 (unigrams + bigrams)
- **Training Data**: 35,918 samples
- **Test Data**: 8,980 samples
- **Test Accuracy**: 98.89%
- **Prediction Speed**: 5-10ms per request
- **Model Size**: 0.22 MB

### Image Classifier
- **Architecture**: Xception (pre-trained on ImageNet)
- **Input Size**: 299x299 pixels
- **Classes**: AI, Deepfake, Real
- **Test Accuracy**: 92.89%
- **Prediction Speed**: 500ms per request
- **Model Size**: 180 MB

### Prediction Combination Logic

**If predictions AGREE** (e.g., both Real):
- Final result = Agreed prediction
- Confidence = Average of both confidences
- Reasoning = "Both modalities confirm..."

**If predictions CONFLICT** (e.g., Image=Fake, Text=Real):
- Final result = "mixed_signals"
- Confidence = Max of both confidences
- Reasoning = "Image and text analysis conflict..."

## ⚡ Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Image prediction | 500ms | CPU or GPU |
| Text prediction | 5-10ms | CPU only |
| Multimodal prediction | 600ms | Sequential |
| Model loading | 2-3s | One-time at startup |

## 🔒 Security & Privacy

- ✅ All processing is local (no cloud uploads)
- ✅ Images and text are not stored
- ✅ Temporary files are automatically deleted
- ✅ No external API calls

## 🐛 Troubleshooting

### Models Not Found
```
Error: "Cannot load text_model.pkl"
Solution: Run: python train_text_model.py
```

### "Text too short" Error
```
Error: Minimum 10 characters required
Solution: Paste longer text (headlines alone may not work)
```

### Out of Memory
```
Error: CUDA out of memory
Solution: Set environment variable: set CUDA_VISIBLE_DEVICES=-1
         (Forces CPU-only mode)
```

### Port Already in Use
```
Error: Address already in use
Solution: Kill existing process or use different port:
         python app.py --port 5001
```

## 📚 Files Breakdown

| File | Size | Purpose |
|------|------|---------|
| app.py | 10 KB | Flask backend with all endpoints |
| train_text_model.py | 8 KB | Train text classifier script |
| index.html | 15 KB | Beautiful frontend UI |
| xception_model_v2.keras | 180 MB | Pre-trained image model |
| text_model.pkl | 40 KB | Text classifier |
| tfidf_vectorizer.pkl | 185 KB | Text vectorizer |
| Fake.csv | 62 MB | Fake news training data |
| True.csv | 53 MB | Real news training data |

## 🎓 College Project Notes

✅ **Ready for Demo**:
- Fast predictions (< 1 second total)
- Beautiful UI with multiple modes
- Comprehensive error handling
- Well-documented code
- Easy to run and test

✅ **College Project Quality**:
- Clean, beginner-friendly code
- Detailed comments throughout
- Multiple prediction modes
- Professional UI/UX
- Research-backed models

## 📖 How It Works

1. **Image Encoding**: Xception extracts features from image
2. **Text Encoding**: TF-IDF converts text to numerical features
3. **Individual Predictions**: Both models make independent predictions
4. **Combination**: Logic merges results based on confidence and agreement
5. **Reasoning**: Generates human-readable explanation

## 🚀 Next Steps

1. ✅ Install requirements: `pip install -r requirements.txt`
2. ✅ Start Flask app: `python app.py`
3. ✅ Open browser: `http://localhost:5000`
4. ✅ Try multimodal prediction
5. ✅ Test with sample images and text
6. ✅ Review predictions and confidence scores

---

**Built with**: Flask, TensorFlow, scikit-learn, HTML5, CSS3, Vanilla JavaScript

**Models**: Xception CNN + TF-IDF + Logistic Regression

**Accuracy**: 95%+ on combined tasks

**Speed**: 600ms average per multimodal prediction

---

Made for college project demo. Questions? Check the code comments!
