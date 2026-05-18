# Quick Start Guide - Multimodal Fake News Detector

## ⚡ Run in 60 Seconds

### Step 1: Start the Server
```bash
python app.py
```

You should see:
```
WARNING:tensorflow:From ...
 * Running on http://127.0.0.1:5000
```

### Step 2: Open Your Browser
Go to: **http://localhost:5000**

### Step 3: Try Multimodal Analysis

#### Option A: Multimodal Tab (Recommended)
1. Click "Multimodal" tab
2. Upload any image file
3. Paste news text (minimum 10 characters):
   ```
   "Breaking: New renewable energy source discovered by researchers"
   ```
4. Click "Predict Multimodal"
5. See results with image + text + combined prediction

#### Option B: Image Only
1. Click "Image Only" tab
2. Upload any image
3. Click "Predict Image"
4. Get AI/Deepfake/Real classification

#### Option C: Text Only
1. Click "Text Only" tab
2. Paste news article text
3. Click "Predict Text"
4. Get Fake/Real classification

## 📊 Expected Results

### Image Model
- **Input**: JPG, PNG, any image
- **Output**: AI (2.3%), Deepfake (5.2%), Real (92.5%)
- **Time**: 500ms

### Text Model
- **Input**: "Scientists discover..."
- **Output**: Fake (14.7%), Real (85.3%)
- **Time**: 5-10ms

### Combined
- **Input**: Image + Text
- **Output**: Final verdict with reasoning
- **Time**: 600ms

## 🔥 Test Cases

### Test 1: Multimodal - Agreement
```
Image: Upload test1.jpg
Text: "New healthcare policy announced by government"
Result: Should show REAL (both agree)
```

### Test 2: Multimodal - Conflict
```
Image: Upload test2.jpg
Text: "Aliens discovered living under ocean"
Result: Should show MIXED_SIGNALS (conflict)
```

### Test 3: Text-Only
```
Text: "Donald Trump becomes President of Mars"
Result: Should show FAKE (88%)
```

### Test 4: Image-Only
```
Image: Upload any test*.jpg
Result: Shows AI/Deepfake/Real classification
```

## 📱 Using the API

### From Terminal (Linux/Mac)

```bash
# Test text prediction
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "Scientists announce breakthrough in renewable energy"}' \
  http://localhost:5000/predict-text

# Test image prediction
curl -X POST \
  -F "file=@test.jpg" \
  http://localhost:5000/predict-image

# Test multimodal prediction
curl -X POST \
  -F "image=@test.jpg" \
  -F "text=News article here" \
  http://localhost:5000/predict-multimodal
```

### From Python

```python
import requests

# Text prediction
response = requests.post(
    'http://localhost:5000/predict-text',
    json={'text': 'Your news text here'}
)
print(response.json())

# Image prediction
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/predict-image',
        files={'file': f}
    )
print(response.json())
```

## 🎯 Example Flow

1. **User uploads news image** → Image model processes
2. **User enters article text** → Text model processes
3. **System compares results**:
   - If both say "Real" → Final: REAL
   - If one says "Fake" → Final: FAKE or MIXED
4. **Display reasoning**: "Image: AI (92%), Text: Real (78%) - CONFLICT"

## ⚙️ Configuration

### Text Prediction (if you need to retrain)
```bash
python train_text_model.py
```

Output:
```
Step 1: Loading CSV files...
  Total samples: 44,898
  Fake: 23,481, Real: 21,417

...training...

TRAINING COMPLETE!
Test Accuracy: 98.89%
```

### Check Metrics
Visit: **http://localhost:5000/metrics**

JSON response with accuracy scores

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| "Port 5000 already in use" | Kill process: `lsof -ti:5000 \| xargs kill -9` |
| "Module not found" | Install: `pip install -r requirements.txt` |
| "Models not found" | Verify files exist or run: `python train_text_model.py` |
| "Image too large" | Resize to < 5MB |
| "Text too short" | Need minimum 10 characters |

## 📝 Sample Predictions

### Sample 1: Real News + Real Image
```
Text: "Apple Inc. announces quarterly earnings report"
Image: Official Apple photo
Result: REAL (92% confidence)
```

### Sample 2: Fake News + Fake Image
```
Text: "Government hides secret alien bases"
Image: AI-generated image
Result: FAKE (95% confidence)
```

### Sample 3: Mixed Signals
```
Text: "Scientists discover new energy"
Image: AI-generated image
Result: MIXED_SIGNALS (87% confidence)
Reason: Text authentic but image suspicious
```

## 📊 Performance

```
Model Loading:     2-3 seconds (one time)
Text Prediction:   5-10 ms
Image Prediction:  500 ms
Multimodal:        600 ms total

Total Model Size:  ~190 MB
Text Model Size:   225 KB
Image Model Size:  180 MB
```

## ✅ Checklist Before Demo

- [ ] Python installed (3.8+)
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Models exist (xception_model_v2.keras, text_model.pkl, tfidf_vectorizer.pkl)
- [ ] App runs without errors: `python app.py`
- [ ] Browser opens to http://localhost:5000
- [ ] Upload image works
- [ ] Text input works
- [ ] Predictions are fast (< 1 second)
- [ ] Results display correctly

## 🎓 For Your College Project

**What to show:**
1. Start the app
2. Show the beautiful UI with tabs
3. Upload an image
4. Paste text
5. Get instant multimodal prediction
6. Show reasoning
7. Test different scenarios
8. Explain model architecture
9. Show API endpoints working

**Key Points to Mention:**
- 98.89% text accuracy
- 92.89% image accuracy
- ~95% combined accuracy
- Real-time predictions
- Professional UI/UX
- Multiple modalities

---

**Ready to demo!** 🚀

Run: `python app.py`

Then visit: http://localhost:5000
