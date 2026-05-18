"""
Train a lightweight text classifier using TF-IDF + Logistic Regression
This creates fast, small models (~10MB) suitable for real-time predictions

Usage: python train_text_model.py
Output: text_model.pkl and tfidf_vectorizer.pkl
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import time

print("=" * 70)
print("TEXT CLASSIFIER TRAINING - TF-IDF + Logistic Regression")
print("=" * 70)
print()

# =====================================================================
# STEP 1: LOAD DATA
# =====================================================================
print("Step 1: Loading CSV files...")
start_time = time.time()

try:
    # Load fake news
    print("  Loading Fake.csv...")
    fake_df = pd.read_csv("Fake.csv")
    fake_df['label'] = 0  # 0 = Fake

    # Load real news
    print("  Loading True.csv...")
    true_df = pd.read_csv("True.csv")
    true_df['label'] = 1  # 1 = Real

    # Combine
    df = pd.concat([fake_df, true_df], ignore_index=True)
    print(f"  Total samples: {len(df):,}")
    print(f"  Fake: {(df['label'] == 0).sum():,}, Real: {(df['label'] == 1).sum():,}")

except Exception as e:
    print(f"ERROR loading files: {e}")
    exit(1)

# =====================================================================
# STEP 2: PREPARE TEXT DATA
# =====================================================================
print("\nStep 2: Preparing text data...")

# Combine title and text for better features
df['combined_text'] = (df['title'].fillna('') + ' ' + df['text'].fillna('')).str.lower()

# Remove empty texts
df = df[df['combined_text'].str.len() > 10]
print(f"  After cleaning: {len(df):,} samples")

X = df['combined_text'].values
y = df['label'].values

# Split into train/test (80/20)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"  Train set: {len(X_train):,}")
print(f"  Test set: {len(X_test):,}")

# =====================================================================
# STEP 3: CREATE TF-IDF VECTORIZER
# =====================================================================
print("\nStep 3: Creating TF-IDF vectorizer...")
print("  Parameters:")
print("    - max_features: 5000")
print("    - ngram_range: (1, 2)")
print("    - min_df: 2")
print("    - max_df: 0.8")

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.8,
    lowercase=True,
    stop_words='english'
)

print("  Fitting vectorizer on training data...")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print(f"  Vocabulary size: {len(vectorizer.get_feature_names_out()):,} features")
print(f"  Train matrix shape: {X_train_tfidf.shape}")
print(f"  Test matrix shape: {X_test_tfidf.shape}")

# =====================================================================
# STEP 4: TRAIN LOGISTIC REGRESSION
# =====================================================================
print("\nStep 4: Training Logistic Regression classifier...")
print("  Parameters:")
print("    - max_iter: 1000")
print("    - solver: lbfgs")

classifier = LogisticRegression(
    max_iter=1000,
    solver='lbfgs',
    random_state=42,
    n_jobs=-1  # Use all cores
)

print("  Training (this may take a minute)...")
classifier.fit(X_train_tfidf, y_train)
print("  Training complete!")

# =====================================================================
# STEP 5: EVALUATE MODEL
# =====================================================================
print("\nStep 5: Evaluating model performance...")

# Train predictions
y_train_pred = classifier.predict(X_train_tfidf)
train_accuracy = accuracy_score(y_train, y_train_pred)

# Test predictions
y_test_pred = classifier.predict(X_test_tfidf)
test_accuracy = accuracy_score(y_test, y_test_pred)
precision = precision_score(y_test, y_test_pred)
recall = recall_score(y_test, y_test_pred)
f1 = f1_score(y_test, y_test_pred)

print(f"\nTRAINING METRICS:")
print(f"  Accuracy: {train_accuracy*100:.2f}%")

print(f"\nTEST METRICS:")
print(f"  Accuracy:  {test_accuracy*100:.2f}%")
print(f"  Precision: {precision*100:.2f}%")
print(f"  Recall:    {recall*100:.2f}%")
print(f"  F1-Score:  {f1*100:.2f}%")

# Confusion matrix
cm = confusion_matrix(y_test, y_test_pred)
print(f"\nCONFUSION MATRIX:")
print(f"  True Negatives (Correctly identified as Fake):  {cm[0, 0]:,}")
print(f"  False Positives (Fake classified as Real):      {cm[0, 1]:,}")
print(f"  False Negatives (Real classified as Fake):      {cm[1, 0]:,}")
print(f"  True Positives (Correctly identified as Real):  {cm[1, 1]:,}")

# =====================================================================
# STEP 6: SAVE MODELS
# =====================================================================
print("\nStep 6: Saving models...")

# Save vectorizer
vectorizer_path = "tfidf_vectorizer.pkl"
with open(vectorizer_path, 'wb') as f:
    pickle.dump(vectorizer, f)
print(f"  Vectorizer saved: {vectorizer_path}")

# Save classifier
classifier_path = "text_model.pkl"
with open(classifier_path, 'wb') as f:
    pickle.dump(classifier, f)
print(f"  Classifier saved: {classifier_path}")

# Get file sizes
import os
vec_size = os.path.getsize(vectorizer_path) / (1024*1024)
clf_size = os.path.getsize(classifier_path) / (1024*1024)
print(f"\nMODEL SIZES:")
print(f"  Vectorizer: {vec_size:.2f} MB")
print(f"  Classifier: {clf_size:.2f} MB")
print(f"  Total: {vec_size + clf_size:.2f} MB")

# =====================================================================
# STEP 7: TEST PREDICTION SPEED
# =====================================================================
print("\nStep 7: Testing prediction speed...")

sample_texts = [
    "The government announces new health policy reforms",
    "Scientists discover aliens in Mars base",
    "Stocks rise as tech companies report earnings"
]

print("  Sample predictions:")
for text in sample_texts:
    start = time.time()
    X_sample = vectorizer.transform([text])
    pred = classifier.predict(X_sample)[0]
    prob = classifier.predict_proba(X_sample)[0]
    elapsed = (time.time() - start) * 1000

    prediction = "REAL" if pred == 1 else "FAKE"
    confidence = max(prob) * 100
    print(f"    - '{text[:40]}...' -> {prediction} ({confidence:.1f}%) in {elapsed:.1f}ms")

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 70)
print("TRAINING COMPLETE!")
print("=" * 70)
print(f"[OK] Models saved and ready for use")
print(f"[OK] Test accuracy: {test_accuracy*100:.2f}%")
print(f"[OK] Prediction speed: ~5-10ms per request")
print(f"[OK] Model size: ~{vec_size + clf_size:.2f} MB (vs 250MB for BERT)")
print(f"\nYou can now run: python app.py")
print("=" * 70)
